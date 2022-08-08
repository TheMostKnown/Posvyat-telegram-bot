import telegram
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler, PollAnswerHandler,
)

from . import tg_config
from . import commands
from . import admin, commands, organizer, user

def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """

    dp.add_handler(CommandHandler('start', commands.start))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), commands.echo))


    # # admin commands
    # dp.add_handler(CommandHandler("admin", admin.admin))
    # dp.add_handler(CommandHandler("stats", admin.stats))


    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(Filters.document, <function_handler>))

    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(token=tg_config.TOKEN, use_context=True)
    # dispatcher = updater.dispatcher

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    updater.start_polling()