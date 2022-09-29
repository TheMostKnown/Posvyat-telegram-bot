# -*- coding: utf-8 -*-

import datetime
import logging
from os import stat
import re


import telegram
from telegram.ext import ConversationHandler, CallbackContext

from django.utils import timezone
from tgbot.handlers import static_text
from tgbot.models import User, Issue, Room, Guest, Organizer, OrganizerSchedule
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
    username = update.message.from_user['username']
    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return
        
    if not user.is_admin:
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
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        u = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return
    
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
    LIMIT_ISSUE = 3
    username = update.message.from_user['username']
    try:
        user = Guest.objects.get(tg_tag=username)
    except Guest.DoesNotExist:
        try:
            user = Organizer.objects.get(tg_tag=username)
        except Organizer.DoesNotExist:
            return
    # spam-filter
    if Issue.objects.filter(tg_tag=user.tg_tag).exclude(status=md.SET_FIXED).count() >= LIMIT_ISSUE:
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
    Issue(
        tg_tag=update.message.from_user['username'],
        desc=update.message.text
    ).save()

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

def time_to_move(context: CallbackContext):
    # функция которая отправляет пользователю уведомление, что скоро переход
    # запускается после ввода пользователем /start

    chat_id = context.job.context['id']
    tg_tag = context.job.context['tag']

    dt = datetime.datetime.now() #получаем текущее время

    day_now = f"{dt.day}.{dt.month}.{dt.year}" # формат вида 1.10.2022 
    time = dt.time().strftime('%H:%M') # формат вида 07:15
    time_now = datetime.datetime.strptime(time, '%H:%M')
    print("Сейчас "+ time)


    org = OrganizerSchedule.objects.filter(tg_tag=tg_tag, date=day_now)
    for item in org:
        print("item")
        print("время ", item.start_time)
        print("задача ", item.desс)
        if datetime.datetime.strptime(item.start_time, '%H:%M') - time_now < datetime.timedelta(minutes = 15):
            print("прошел проверку, вернул задачу ", item.desс)
            return context.bot.send_message(
                chat_id = chat_id,
                text = f"Смена деятельности с {item.start_time} - {item.desс}"
            )

    
    


def commands_list(update, context):
    text = 'Привет! Вот доступные тебе команды: \n' + static_text.common_comands

    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    # Для информирования оргов о времени перейти на новую точку
    # first - когда первый раз запустится задача
    # в 7.50 утра 1.10 октября 2022
    # будет запускаться с интервалом в 30 минут
    # last - задача будет запускаться до
    # 15.50 2.10 2022

    context.job_queue.run_repeating(
        callback = time_to_move,
        interval = datetime.timedelta(minutes=30),
        first = datetime.datetime(
            year = 2022,
            month = 10,
            day = 1,
            hour=7, 
            minute = 50,
            ),
        last = datetime.datetime(
            year = 2022,
            month = 10,
            day = 2,
            hour=15, 
            minute = 50,
        ),
        context = {'id':user_id, 'tag':username}
    )
    try:
        user = Organizer.objects.get(tg_tag=username)
        text += static_text.organizer_commands
    except Organizer.DoesNotExist:
        return context.bot.send_message(user_id, text=text)
    if user.is_admin:
        text += static_text.secret_admin_commands
    return context.bot.send_message(user_id, text=text)
    