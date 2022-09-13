# -*- coding: utf-8 -*-

import datetime
import logging
import re
import telegram
from telegram.ext import ConversationHandler

from django.utils import timezone
from tgbot.handlers import static_text
from tgbot.models import User, Issue, Room
from tgbot.utils import extract_user_data_from_update
from tgbot.handlers.keyboard_utils import make_keyboard_for_start_command, keyboard_confirm_decline_broadcasting
from tgbot.handlers.utils import handler_logging
from tgbot.handlers import manage_data as md

logger = logging.getLogger('default')
logger.info("Command handlers check!")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")


def echo(update, context):
    # добавим в начало полученного сообщения строку 'ECHO: '
    text = 'ECHO: ' + update.message.text
    # `update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


@handler_logging()
def command_start(update, context):
    user, created = User.get_user_and_created(update, context)

    payload = context.args[0] if context.args else user.deep_link  # if empty payload, check what was stored in DB
    text = 'Hello!'

    user_id = extract_user_data_from_update(update)['user_id']
    context.bot.send_message(chat_id=user_id, text=text, reply_markup=make_keyboard_for_start_command())


def stats(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    text = f"""
        *Users*: {User.objects.count()}
        *24h active*: {User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text, 
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


def broadcast_command_with_message(update, context):
    """ Type /broadcast <some_text>. Then check your message in Markdown format and broadcast to users."""
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        text = static_text.broadcast_no_access
        markup = None

    else:
        text = f"{update.message.text.replace(f'{static_text.broadcast_command} ', '')}"
        markup = keyboard_confirm_decline_broadcasting()

    try:
        context.bot.send_message(
            text=text,
            chat_id=user_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=markup
        )
    except telegram.error.BadRequest as e:
        place_where_mistake_begins = re.findall(r"offset (\d{1,})$", str(e))
        text_error = static_text.error_with_markdown
        if len(place_where_mistake_begins):
            text_error += f"{static_text.specify_word_with_error}'{text[int(place_where_mistake_begins[0]):].split(' ')[0]}'"
        context.bot.send_message(
            text=text_error,
            chat_id=user_id
        )

def issue(update, context):
    u = User.get_user(update, context)
    if u.is_banned:
        return ConversationHandler.END
    if Issue.objects.filter(tg_tag = u.username).exclude(status = md.SET_FIXED).count() >= 3:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=static_text.issue_limit
        )
        return ConversationHandler.END
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=static_text.support_start
    )
    return md.ISSUE_MESSAGE_WAITING

def issue_message(update, context):
    # тут добавление сообщения в бд
    Issue(tg_tag = update.message.from_user['username'],
                desc = update.message.text).save()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=static_text.support_send
    )
    return ConversationHandler.END

def issue_cancel(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=static_text.support_cancel
    )
    return ConversationHandler.END
