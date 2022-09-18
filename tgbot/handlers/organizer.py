
from tgbot.handlers import static_text as st
from tgbot.models import Organizer, Room, Guest
from tgbot.handlers import static_text as st

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
    
    depart = context.args[0].lower()
    all_orgs = Organizer.objects.all()
    orgs_of_dep = list()
    for org in all_orgs:
        deps_list = org.department.split(",")
        if depart in deps_list:
            orgs_of_dep.append(org)
    
    if len(orgs_of_dep) == 0:
        return context.bot.send_message(user_id, text=st.depart_mistake)
    # to be continued
