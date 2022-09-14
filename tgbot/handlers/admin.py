import datetime
import telegram

from django.utils.timezone import now

from tgbot.handlers import static_text as st
from tgbot.models import User, Issue
from tgbot.utils import extract_user_data_from_update
from tgbot.handlers import keyboard_utils as kb

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
    DESC_LIMIT = 40
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']
    if not u.is_admin:
        return
    if len(context.args) == 0:
        issues_query = Issue.objects.exclude(status='F').order_by('id')
        text = ""
        if issues_query.count() == 0:
            text = st.error_no_unsolved_issue
        for temp in issues_query:
            text += (str(temp.id) + ". " + temp.desc[:DESC_LIMIT])
            if len(temp.desc) > DESC_LIMIT:
                text += "..."
            text += "\n"
        context.bot.send_message(user_id, text=text)
    else:
        if not context.args[0].isdigit():
            return context.bot.send_message(user_id, text=st.error_issue_arg)
        try:
            current_issue = Issue.objects.get(id = int(context.args[0]))
        except Issue.DoesNotExist:
            return context.bot.send_message(user_id, text=st.error_no_issue)
        context.bot.send_message(
            user_id, text=str(current_issue),
            disable_web_page_preview = True,
            reply_markup = kb.keyboard_issue_set_status(current_issue.status),
        )
        

