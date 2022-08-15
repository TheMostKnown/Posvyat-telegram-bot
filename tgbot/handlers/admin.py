import telegram
from tgbot.filters import filters
from tgbot.handlers import static_text as st



def admin(update, context):
    """ Show help info about all secret admins commands """
    user_id = update.message.chat.id
    if not filters.is_admin(user_id):
        return

    return update.message.reply_text(f'{st.secret_level}\n{st.secret_admin_commands}')