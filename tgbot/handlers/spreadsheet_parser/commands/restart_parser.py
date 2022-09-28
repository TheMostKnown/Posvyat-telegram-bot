from dtb.settings import GOOGLE_TABLE_ID, GOOGLE_CREDS_PATH, GOOGLE_TOKEN_PATH
from tgbot.handlers.spreadsheet_parser.commands.export_to_db import get_init_data
from tgbot.models import Organizer
from tgbot.handlers import static_text as st


def restart_parser(update, context):
    username = update.message.from_user['username']
    user_id = update.message.from_user['id']

    try:
        user = Organizer.objects.get(tg_tag=username)
    except Organizer.DoesNotExist:
        return

    if not user.is_admin:
        return context.bot.send_message(user_id, text=st.notification_no_rights)

    get_init_data(
        spreadsheet_id=GOOGLE_TABLE_ID,
        creds_file_name=GOOGLE_CREDS_PATH,
        token_file_name=GOOGLE_TOKEN_PATH
    )

    print('Successful Parsing!')

    return context.bot.send_message(user_id, text=st.parser_notification_success)
