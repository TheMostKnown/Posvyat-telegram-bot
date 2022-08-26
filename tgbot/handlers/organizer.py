
from filters import filters
from handlers import static_text as st


def organizer(update, context):
    """ Show help info about all secret admins commands """
    user_id = update.message.chat.id
    if not filters.is_organizer(user_id):
        return

    return update.message.reply_text(f'{st.secret_level}\n{st.secret_organizer_commands}')