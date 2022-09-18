
from tgbot.handlers import static_text as st
from tgbot.models import Organizer

def organizer(update, context):
    """ Show help info about all secret admins commands """
    user_id = update.message.chat.id
    # if not filters.is_organizer(user_id):
    #     return

    return update.message.reply_text(f'{st.secret_level}\n{st.secret_organizer_commands}')

def room_info(update, context):
    username = update.message.from_user['username']
    try:
        user = Organizer.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return