from create_bot import bot
from tgbot.handlers import commands

commands.register_handlers_commands(bot)
# admin.register_handlers_admin(bot)
# user.register_handlers_user(bot)
# organizer.register_handlers_organizer(bot)

if __name__ == "__main__":
    bot.polling(none_stop=True)
    # run_pooling()