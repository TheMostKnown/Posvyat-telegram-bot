from create_bot import bot

# @bot.message_handler(content_types=['text'])
def repeat(message):
    bot.send_message(message.chat.id, message.text)

def register_handlers_commands(bot):
    bot.register_message_handler(repeat, content_types=['text'])