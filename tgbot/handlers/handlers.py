# -*- coding: utf-8 -*-

import datetime
import logging
import telegram

from django.utils import timezone

from tgbot.handlers import commands
from tgbot.handlers import static_text as st
from tgbot.handlers import manage_data as md
from tgbot.handlers import keyboard_utils as kb
from tgbot.handlers.utils import handler_logging
from tgbot.models import Issue, User
from tgbot.utils import convert_2_user_time, extract_user_data_from_update, get_chat_id, str_between_symb

logger = logging.getLogger('default')


@handler_logging()
def btn1_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']

    markup = kb.make_btn_keyboard()
    msg = f'{st.pressed}1'

    context.bot.edit_message_text(
        text=msg,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=markup,
        parse_mode=telegram.ParseMode.MARKDOWN,
    )


@handler_logging()
def btn2_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']

    markup = kb.make_btn_keyboard()
    msg = f'{st.pressed}2'

    context.bot.edit_message_text(
        text=msg,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=markup,
        parse_mode=telegram.ParseMode.MARKDOWN,
    )


@handler_logging()
def btn3_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']

    markup = kb.make_btn_keyboard()
    msg = f'{st.pressed}3'

    context.bot.edit_message_text(
        text=msg,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=markup,
        parse_mode=telegram.ParseMode.MARKDOWN,
    )


@handler_logging()
def back_to_main_menu_handler(update, context):  # callback_data: BUTTON_BACK_IN_PLACE variable from manage_data.py
    user, created = User.get_user_and_created(update, context)

    payload = context.args[0] if context.args else user.deep_link  # if empty payload, check what was stored in DB
    text = st.welcome

    user_id = extract_user_data_from_update(update)['user_id']
    context.bot.edit_message_text(
        chat_id=user_id,
        text=text,
        message_id=update.callback_query.message.message_id,
        reply_markup=kb.make_keyboard_for_start_command(),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


@handler_logging()
def secret_level(update, context): #callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = "Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
           "*Users*: {user_count}\n" \
           "*24h active*: {active_24}".format(
            user_count=User.objects.count(),
            active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def broadcast_decision_handler(update, context): #callback_data: CONFIRM_DECLINE_BROADCAST variable from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in Markdown style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(md.CONFIRM_DECLINE_BROADCAST):]
    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    entities = update.callback_query.message.entities
    text = update.callback_query.message.text
    if broadcast_decision == md.CONFIRM_BROADCAST:
        admin_text = st.msg_sent,
        user_ids = list(User.objects.all().values_list('user_id', flat=True))
        # broadcast_message.delay(user_ids=user_ids, message=text, entities=entities_for_celery)
    else:
        admin_text = text

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=None if broadcast_decision == md.CONFIRM_BROADCAST else entities
    )

def btn_set_status(update, context):
    new_status = update.callback_query.data
    issue_id = int(str_between_symb(update.callback_query.message.text, '#', '\n')) #Cringe...
    issue = Issue.objects.get(id = issue_id)
    issue.status = new_status
    issue.save()
    context.bot.edit_message_text(
        text=str(issue),
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        reply_markup = kb.keyboard_issue_set_status(new_status),
        disable_web_page_preview = True,
    )

def btn_get_issues_from_user(update, context):
    issue_id = int(str_between_symb(update.callback_query.message.text, '#', '\n'))
    user_tag = Issue.objects.get(id = issue_id).tg_tag
    issues_query = Issue.objects.filter(tg_tag = user_tag).exclude(status = md.SET_FIXED)
    if issues_query.count() == 0:
        return context.bot.send_message(chat_id = update.effective_chat.id, text = st.no_unsolved_issue)
    context.bot.send_message(chat_id = update.effective_chat.id, text = st.users_issues_intro)
    for issue in issues_query:
        context.bot.send_message(
            text=str(issue),
            chat_id=update.callback_query.message.chat_id,
            reply_markup = kb.keyboard_issue_set_status(issue.status),
            disable_web_page_preview = True,
        )