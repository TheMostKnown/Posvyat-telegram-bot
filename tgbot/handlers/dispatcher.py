# -*- coding: utf-8 -*-

"""Telegram event handlers."""

from logging import Filter
from tokenize import group
import telegram

from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler, PollAnswerHandler,
    ConversationHandler,
)

# from celery.decorators import task  # event processing in async mode

from dtb.settings import TELEGRAM_TOKEN

from tgbot.handlers import admin, commands, files, location, organizer
from tgbot.handlers.commands import broadcast_command_with_message
from tgbot.handlers import handlers as hnd
from tgbot.handlers import manage_data as md
from tgbot.handlers.static_text import broadcast_command
from tgbot.handlers.manage_data import ISSUE_MESSAGE_WAITING


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """

    dp.add_handler(CommandHandler("start", commands.command_start))
    dp.add_handler(CommandHandler("help", commands.commands_list))
    # admin commands
    dp.add_handler(CommandHandler("admin", admin.admin))
    dp.add_handler(CommandHandler("stats", admin.stats))

    dp.add_handler(CommandHandler("get_iss", admin.get_issues))
    dp.add_handler(CallbackQueryHandler(hnd.btn_set_status, pattern=f'^{md.SET_IN_PROGRESS}|{md.SET_NOT_FIXED}|{md.SET_FIXED}'))
    dp.add_handler(CallbackQueryHandler(hnd.btn_all_one_issue, pattern=f'^{md.SET_ONE_OR_ALL_ISS}'))
    dp.add_handler(CallbackQueryHandler(hnd.btn_set_all_issues, pattern=f'^{md.SET_ALL_ISS}'))
    dp.add_handler(CallbackQueryHandler(hnd.btn_get_issues_from_user, pattern=f'^{md.GET_ALL_ISS}'))

    dp.add_handler(CommandHandler("delete_issues", admin.delete_issues))
    dp.add_handler(CallbackQueryHandler(hnd.btn_delete_issues, pattern=f'^{md.CONFIRM_DELETING}|{md.DECLINE_DELETING}'))

    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))
    # organizer command
    dp.add_handler(CommandHandler("room", organizer.room_info))
    dp.add_handler(CommandHandler("depart", organizer.depart_orgs))
    dp.add_handler(CommandHandler("depart_now", organizer.depart_orgs_current_moment))
    # base buttons
    dp.add_handler(CallbackQueryHandler(hnd.btn1_hnd, pattern=f'^{md.BTN_1}'))
    dp.add_handler(CallbackQueryHandler(hnd.btn2_hnd, pattern=f'^{md.BTN_2}'))
    dp.add_handler(CallbackQueryHandler(hnd.btn3_hnd, pattern=f'^{md.BTN_3}'))

    dp.add_handler(CallbackQueryHandler(hnd.back_to_main_menu_handler, pattern=f'^{md.BUTTON_BACK_IN_PLACE}'))

    # location
    dp.add_handler(CommandHandler("ask_location", location.ask_for_location))
    dp.add_handler(MessageHandler(Filters.location, location.location_handler))

    dp.add_handler(CallbackQueryHandler(hnd.secret_level, pattern=f"^{md.SECRET_LEVEL_BUTTON}"))

    dp.add_handler(MessageHandler(Filters.regex(rf'^{broadcast_command} .*'), broadcast_command_with_message))
    dp.add_handler(CallbackQueryHandler(hnd.broadcast_decision_handler, pattern=f"^{md.CONFIRM_DECLINE_BROADCAST}"))
    
    # issues
    dp.add_handler(ConversationHandler(
        # точка входа
        entry_points=[CommandHandler('support', commands.issue)],
        states={
            ISSUE_MESSAGE_WAITING: [
                MessageHandler(Filters.text & ~Filters.command, commands.issue_message),
            ],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', commands.issue_cancel), MessageHandler(Filters.command, commands.issue_cancel)],
        allow_reentry=True,
    ), group=2)

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling(timeout=123)
    updater.idle()


# @task(ignore_result=True)
# def process_telegram_event(update_json):
#     update = telegram.Update.de_json(update_json, bot)
#     dispatcher.process_update(update)


# Global variable - best way I found to init Telegram bot
bot = telegram.Bot(TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]