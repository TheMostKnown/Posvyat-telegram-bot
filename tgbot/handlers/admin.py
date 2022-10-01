import datetime
import telegram
import schedule

from django.utils.timezone import now

from tgbot.handlers import static_text as st
from tgbot.models import Organizer, User, Issue
from tgbot.utils import extract_user_data_from_update
from tgbot.handlers import keyboard_utils as kb
from tgbot.handlers import manage_data as md
from tgbot.models import User, Guest, Organizer

from logs.sending_logs import sending_logs

error = 'Команда не была выполнена из-за неизвестной ошибки, возможно Вы передали неверный аргумент. Пожалуйста, перечитайте документацию по команде /help и попробуйте снова'


def admin(update, context):
    """ Show help info about all secret admins commands """
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
        return

    return update.message.reply_text(f'{st.secret_admin_commands}')


def stats(update, context):
    """ Show help info about all secret admins commands """
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
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


def delete_user(update, context):
    """
        deletes the listed users for the listed reasons
    """
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
        return

    try:
        users_to_ban = []  # список юзеров для удаления
        reasons = []  # список причин удаления
        for arg in context.args:
            if context.args.index(arg) % 2 == 0:
                users_to_ban.append(arg)
            else:
                reasons.append(arg)

        for arg in range(int(len(context.args) / 2)):
            # получение чат айди юзера из бд и отправка ему уведомления об удалении
            user = Guest.objects.get(tg_tag=users_to_ban[arg])
            user = user[0]
            banned_user_text = st.notification_banned_user_reason + f'{reasons[arg]}'
            context.bot.send_message(chat_id=user.chat_id, text=banned_user_text)

            # блокировка юзера в боте
            user.is_banned = True
            user.save()

            # сообщение об успешном выполнении команды
            done = f'Пользователь {users_to_ban[arg]} успешно забанен!'
            context.bot.send_message(user_id, text=done)

    except Exception:
        context.bot.send_message(user_id, text=error)


def get_logs(update, context):
    """
        Sends logs from the main.log and django_request.log files
    """
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
        return

    done = st.notification_command_success

    def send_logs():
        context.bot.send_message(
            user_id,
            text=f'Логи файла main:\n{sending_logs()[0]}\n'
                 f'Логи файла django_request:\n{sending_logs()[1]}'
        )

    try:
        if context.args[0].lower() == 'now':

            context.bot.send_message(
                user_id,
                text=f'Логи файла main:\n{sending_logs()[0]}\n'
                     f'Логи файла django_request:\n{sending_logs()[1]}'
            )

            context.bot.send_message(user_id, text=done)

        elif context.args[1].lower() == 'secs':
            context.bot.send_message(user_id, text=done)
            schedule.every(int(context.args[0])).seconds.do(send_logs)

        elif context.args[1].lower() == 'mins':
            context.bot.send_message(user_id, text=done)
            schedule.every(int(context.args[0])).minutes.do(send_logs)

        elif context.args.lower() == 'hour':
            context.bot.send_message(user_id, text=done)
            schedule.every().hour.do(send_logs)

        elif context.args[1].lower() == 'day':
            context.bot.send_message(user_id, text=done)
            schedule.every().day.at(int(context.args[0])).do(send_logs)

        else:
            raise Exception

    except Exception:
        context.bot.send_message(user_id, text=error)


def replace_org_tag(update, context):
    """
        Replaces the first organizer tag with the second one
    """
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
        return

    try:
        old_tag = context.args[0]
        new_tag = context.args[1]
        done = f'Тег {old_tag} был успешно заменен на тег {new_tag}'

        if len(context.args) > 2:
            raise Exception

        org = Organizer.objects.get(tg_tag=old_tag)
        org = org[0]
        org.tg_tag = new_tag
        org.save()

        context.bot.send_message(user_id, text=done)

    except Exception:
        context.bot.send_message(user_id, text=error)


def info_mailing(update, context):
    """
        Sends a newsletter to all members of a certain department
    """

    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
        return

    try:
        message_text = update.message.text
        start = message_text.find('<') + 1
        end = message_text.find('>')
        text = message_text[start:end]
        department = message_text[message_text.find('>') + 2:]
        done = []
        undone = []

        orgs = []
        for org in Organizer.objects.all():
            if department in org.department:
                orgs.append(org)

        for org in orgs:
            if org.chat_id is not None:
                done.append(org.tg_tag)
                context.bot.send_message(chat_id=org.chat_id, text=text)
            else:
                undone.append(org.tg_tag)

        context.bot.send_message(
            user_id,
            text=st.notification_broadcast_address + f'{", ".join(done)}' + '\n'
                 + st.notification_broadcast_unsucces_address + f'{", ".join(undone)}'
        )
        context.bot.send_message(user_id, text=st.notification_broadcast_success)

    except Exception:
        context.bot.send_message(user_id, text=error)


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
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
        return context.bot.send_message(id=user_id, text=st.notification_no_rights)

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

    if not user.is_admin:
        return context.bot.send_message(id=user_id, text=st.notification_no_rights)

    context.bot.send_message(
        user_id, text=st.delete_issues_choose,
        reply_markup=kb.keyboard_confirm_delete_issue(),
    )
