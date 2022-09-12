import datetime
import telegram

from django.utils.timezone import now

from tgbot.handlers import static_text as st
from tgbot.models import User, Issue
from tgbot.utils import extract_user_data_from_update


def admin(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    return update.message.reply_text(f'{st.secret_level}\n{st.secret_admin_commands}')
    

def stats(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    text = f"""
        *Users*: {User.objects.count()}
        *24h active*: {User.objects.filter(updated_at__gte=now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text, 
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )

def get_issues(update, context):
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']
    if not u.is_admin:
        return
    issues_query = Issue.objects.exclude(status='Fixed')
    for temp in issues_query:
        context.bot.send_message(user_id, text=temp)