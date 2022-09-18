import datetime
import telegram

from django.utils.timezone import now

from tgbot.handlers import static_text as st
from tgbot.models import Organizer, User, Issue
from tgbot.utils import extract_user_data_from_update
from tgbot.handlers import keyboard_utils as kb
from tgbot.handlers import manage_data as md


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
    """" Shows list of unsolved issues in format:
        issue_number -- first DESC_LIMIT symbols of description

        Shows issue's full info you use command with issue's number as argument
        It also allows to change its status with the buttons
    """
    DESC_LIMIT = 40

    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return
        
    if not user.is_admin:
        return

    if len(context.args) == 0:
        issues_query = Issue.objects.exclude(status=md.SET_FIXED).order_by('id')
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
            current_issue = Issue.objects.get(id=int(context.args[0]))
        except Issue.DoesNotExist:
            return context.bot.send_message(user_id, text=st.error_no_issue)

        context.bot.send_message(
            user_id, text=str(current_issue),
            disable_web_page_preview=True,
            reply_markup=kb.keyboard_issue_set_status(current_issue.status),
        )


def delete_issues(update, context):
    """Deletes all solved issues from DataBase"""
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
        return

    context.bot.send_message(
        user_id, text=st.delete_issues_choose,
        reply_markup=kb.keyboard_confirm_delete_issue(),
    )

