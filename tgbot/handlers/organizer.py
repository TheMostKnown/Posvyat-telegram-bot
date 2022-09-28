from copy import deepcopy
from tracemalloc import start
from tgbot.handlers import static_text as st
from tgbot.models import Organizer, Room, Guest, OrganizerSchedule
import datetime as dt
from django.db.models import Max, Min
# from tgbot.handlers.test import handler_message
import telegram
from tgbot.handlers import manage_data as md


def organizer(update, context):
    """ Show help info about all secret admins commands """
    user_id = update.message.chat.id
    # if not filters.is_organizer(user_id):
    #     return

    return update.message.reply_text(f'{st.secret_level}\n{st.secret_organizer_commands}')


def room_info(update, context):
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if len(context.args) == 0:
        return context.bot.send_message(user_id, text=st.room_no_argument)

    room_input = context.args[0]
    try:
        room = Room.objects.get(number=room_input)
    except Room.DoesNotExist:
        return context.bot.send_message(user_id, text=st.room_not_found)

    residents = Guest.objects.filter(room=room.number)
    text = str(room)
    text += "Участники:\n"

    for res in residents:
        text += f"- ФИО: {res.surname} {res.name} {res.patronymic}\n" \
                f"  Номер телефона: {res.phone}\n" \
                f"  ТГ: t.me/{res.tg_tag}\n" \
                f"  ВК: {res.vk_link}\n" \
                f"  Команда: {res.team}\n"

    return context.bot.send_message(user_id, text=text, disable_web_page_preview=True)


def depart_orgs(update, context):
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if len(context.args) == 0:
        return context.bot.send_message(user_id, text=st.depart_no_argument)

    depart = context.args[0].capitalize()

    all_orgs = Organizer.objects.all()
    orgs_of_dep = list()

    for org in all_orgs:
        deps_list = org.department.split(",")
        if depart in deps_list:
            orgs_of_dep.append(org)

    if len(orgs_of_dep) == 0:
        return context.bot.send_message(user_id, text=st.depart_mistake)

    text = f"{st.list_of_orgs_from} {depart}:\n"
    for org in orgs_of_dep:
        text += f"{org.surname} {org.name} t.me/{org.tg_tag}\n"

    return context.bot.send_message(user_id, text=text, disable_web_page_preview=True)


def depart_orgs_current_moment(update, context):
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if len(context.args) == 0:
        return context.bot.send_message(user_id, text=st.depart_now_no_argument)

    depart = context.args[0].capitalize()
    # spell check and auto-fix
    # if depart not in md.DEPART_LIST:
    # depart = handler_message(depart, md.DEPART_LIST)

    all_orgs = Organizer.objects.all()
    orgs_of_dep = list()

    for org in all_orgs:
        deps_list = org.department.split(",")
        if depart in deps_list:
            orgs_of_dep.append(org)

    if len(orgs_of_dep) == 0:
        return context.bot.send_message(user_id, text=st.depart_mistake)

    current_time = dt.datetime.now()
    curr_datetime_str = current_time.strftime("%H:%M:%S %d/%m/%Y")

    text = f"Отдел {depart} в {curr_datetime_str}\n"

    for org in orgs_of_dep:
        event = get_current_event(current_time, org)
        text += f"{org.name} {org.surname} - {event}\n"

    return context.bot.send_message(user_id, text=text)


def schedule(update, context):
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']
    text = ""

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    # user's schedule
    if len(context.args) == 0 or len(context.args) > 2:
        text += "Расписание:\n\n"
        sched = get_schedule(user.tg_tag)
        text += sched
        return context.bot.send_message(user_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

    # schedule by surname and name
    if len(context.args) == 2:
        users = Organizer.objects.filter(
            surname=context.args[0].capitalize(),
            name=context.args[1].capitalize()
        )

        if users.count() == 0:
            users = Organizer.objects.filter(
                surname=context.args[1].capitalize(),
                name=context.args[0].capitalize()
            )

        if users.count() == 0:
            text += st.org_not_found
            org_list = list(Organizer.objects.values_list('surname', flat=True))
            # text += handler_message(context.args[0], org_list)

            return context.bot.send_message(user_id, text=text)

        user = users[0]
        text += f"{user.surname} {user.name}\n\nРасписание\n"
        text += get_schedule(user.tg_tag)

        return context.bot.send_message(user_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

    # schedule by surname or name or tg_tag or vk_link or phone_number
    if len(context.args) == 1:
        input = context.args[0]

        # phone
        users = Organizer.objects.filter(phone=input)

        # tg_tag
        if users.count() == 0:
            users = Organizer.objects.filter(tg_tag=input)

        # vk_link
        if users.count() == 0:
            users = Organizer.objects.filter(vk_link=input)

        input = input.capitalize()

        # surname
        if users.count() == 0:
            users = Organizer.objects.filter(surname=input)

        # name
        if users.count() == 0:
            users = Organizer.objects.filter(name=input)

        # not found at all
        if users.count() == 0:
            text += st.org_not_found
            return context.bot.send_message(user_id, text=text)

        user = users[0]
        text += f"{user.surname} {user.name}\n\nРасписание\n"
        text += get_schedule(user.tg_tag)

        return context.bot.send_message(user_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)


def guest_info(update, context):
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']
    text = ""

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if len(context.args) == 2:
        users = Guest.objects.filter(
            surname=context.args[0].capitalize(),
            name=context.args[1].capitalize()
        )

        if users.count() == 0:
            users = Guest.objects.filter(
                surname=context.args[1].capitalize(),
                name=context.args[0].capitalize()
            )

        if users.count() == 0:
            text += st.guest_not_found
            # org_list = list(Guest.objects.values_list('surname', flat=True))
            # text += handler_message(context.args[0], org_list)

            return context.bot.send_message(user_id, text=text)

        user = users[0]
        text += get_guest_info(user)
        return context.bot.send_message(user_id, text=text)

    if len(context.args) == 1:
        input = context.args[0]

        # phone
        users = Guest.objects.filter(phone=input)

        # tg_tag
        if users.count() == 0:
            users = Guest.objects.filter(tg_tag=input)

        # vk_link
        if users.count() == 0:
            users = Guest.objects.filter(vk_link=input)

        input = input.capitalize()

        # surname
        if users.count() == 0:
            users = Guest.objects.filter(surname=input)

        # name
        if users.count() == 0:
            users = Guest.objects.filter(name=input)

        # not found at all
        if users.count() == 0:
            text += st.guest_not_found
            return context.bot.send_message(user_id, text=text)

        user = users[0]
        text += get_guest_info(user)
        return context.bot.send_message(user_id, text=text)

    if len(context.args) == 0:
        return context.bot.send_message(user_id, text=st.guest_no_arg)

    if len(context.args) > 2:
        return context.bot.send_message(user_id, text=(st.guest_too_much_args + st.guest_no_arg))


def depart_list(update, context):
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']
    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return
    context.bot.send_message(
        user_id,
        text = '\n'.join(md.DEPART_LIST)
        )

def get_team(update, context):
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']
    text = ""
    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return
    
    if len(context.args) == 0:
        return context.bot.send_message(user_id, text=st.team_no_arg)
    if not context.args[0].isdigit():
        return context.bot.send_message(user_id, text=st.error_issue_arg)
    
    teammates = Guest.objects.filter(team=context.args[0])

    if teammates.count() == 0:
        return context.bot.send_message(user_id, text=st.team_not_found)
    text += f"Команда №{context.args[0]}\n"
    for guest in teammates:
        text += f"{guest.surname} {guest.name} {guest.patronymic} t.me/{guest.tg_tag}\n"
    return context.bot.send_message(user_id, text=text)


def get_current_event(current_time: dt.datetime, org: Organizer):
    if current_time.minute >= 30:
        current_time = current_time.replace(minute=30)
    else:
        current_time = current_time.replace(minute=0)

    # For test use commented vars instead of actual
    # start_time = dt.time(minute=30, hour = 9).strftime("%H:%M")
    # date = dt.date(day=2, month=10, year=2022).strftime("%d.%m.%Y")

    start_time = current_time.strftime("%H:%M")
    date = current_time.strftime("%d.%m.%Y")

    if date[0] == '0':
        date = date[1:]
    if start_time[0] == '0':
        start_time = start_time[1:]

    events = OrganizerSchedule.objects.filter(tg_tag=org.tg_tag, start_time=start_time, date=date)

    if events.count() == 0:
        return "no event"
    return events[0].desc


def get_schedule(tg_tag: str):
    current_time = dt.datetime.now()
    events = OrganizerSchedule.objects.filter(tg_tag=tg_tag)
    sched = ''
    if events.count() == 0:
        return "No events\n"
    
    if current_time.minute >= 30:
        current_time = current_time.replace(minute=30)
    else:
        current_time = current_time.replace(minute=0)
    
    start_time = current_time.strftime("%H:%M")
    date = current_time.strftime("%d.%m.%Y")

    # For test use commented vars instead of actual
    # start_time = dt.time(minute=30, hour = 9).strftime("%H:%M")
    # date = dt.date(day=2, month=10, year=2022).strftime("%d.%m.%Y")

    
    events.filter(date__gte=date)
    events.exclude(date=date, start_time__lt=start_time)
    events.order_by('date','start_time')

    if events.count() == 0:
        return "No event"
    
    current_action = events[0].desc
    current_start_time = events[0].start_time
    current_start_date = events[0].date
    current_end_time = events[0].finish_time

    for event in events[1:]:
        if current_action == event.desc:
            current_end_time = event.finish_time

        else:
            day = 1 if current_start_date == md.FIRST_DAY else 2
            sched += f'*{current_action}* в {day} день с {current_start_time} до {current_end_time}\n'
            current_action = event.desc
            current_start_time = event.start_time
            current_start_date = event.date
            current_end_time = event.finish_time

    sched += f'*{current_action}* в {day} день с {current_start_time} до ...'

    return sched


def get_guest_info(guest: Guest):
    info = f"ФИО: {guest.surname} {guest.name} {guest.patronymic}\n" \
           f"ТГ: t.me/{guest.tg_tag}\n" \
           f"ВК: {guest.vk_link}\n" \
           f"Номер телефона: {guest.phone}\n" \
           f"Комната: {guest.room}\n"

    if guest.room != '':
        neighbors = Guest.objects.filter(room=guest.room).exclude(id=guest.id)

        info += f"Соседи:\n"
        for neig in neighbors:
            info += f"- {neig.surname} {neig.name} {neig.patronymic}\n"

    info += f"Команда: {guest.team}\n"

    return info
