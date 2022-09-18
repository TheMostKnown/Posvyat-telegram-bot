
from tgbot.handlers import static_text as st
from tgbot.models import Organizer, Room, Guest, OrganizerSchedule
import datetime as dt
from django.db.models import Max, Min

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
        room = Room.objects.get(number = room_input)
    except Room.DoesNotExist:
        return context.bot.send_message(user_id, text=st.room_not_found)
    
    residents = Guest.objects.filter(room = room.number)
    if (residents.count() == 0):
        residents = Organizer.objects.filter(room = room.number)
    text = str(room)
    text += "Жители:\n"
    for res in residents:
        text += f"{res.surname} {res.name} {res.patronymic} t.me/{res.tg_tag} {res.vk_link}\n"
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
    
    depart = context.args[0]
    #TODO add "spellchecker" or lower() to depart

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
        return context.bot.send_message(user_id, text=st.depart_no_argument)
    
    depart = context.args[0]
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


def get_current_event(current_time: dt.datetime, org: Organizer):
    POSVYAT_FIRST_DATE = "18/09/2022"
    POSVYAT_SECOND_DATE = "19/09/2022"
    date = current_time.strftime("%d/%m/%Y")
    if date != POSVYAT_FIRST_DATE and date != POSVYAT_SECOND_DATE:
        return "no event1"
    curr_time_str = current_time.strftime("%H:%M")
    print(curr_time_str)
    start_time = '' + curr_time_str
    print(curr_time_str[3])
    print(curr_time_str[4])
    if curr_time_str[3] in ('3', '4', '5'):
        start_time[3] = '3'
    else:
        start_time[3] = '0'
    start_time[4] = '0'
    print(start_time)
    events = OrganizerSchedule.objects.filter(tg_tag = org.tg_tag, start_time = start_time)
    if events.count() == 0:
        return "no event2"
    """if date == POSVYAT_SECOND_DATE:
        event = events.get(id=Max('id')).desc
    else:
        event = events.get(id=Min('id')).desc"""
    event = "no ev3"
    return event

