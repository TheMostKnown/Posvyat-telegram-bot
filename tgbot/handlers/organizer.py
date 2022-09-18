
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
