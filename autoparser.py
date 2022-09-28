import django
import os
import schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from tgbot.handlers.spreadsheet_parser.commands.export_to_db import get_init_data
from dtb.settings import GOOGLE_TABLE_ID, GOOGLE_TOKEN_PATH, GOOGLE_CREDS_PATH


print('Initialize autoparser')

parsing_time = 2


def autoparsing():
    print('PROCESSING AUTOPARSING!')
    get_init_data(
        spreadsheet_id=GOOGLE_TABLE_ID,
        creds_file_name=GOOGLE_CREDS_PATH,
        token_file_name=GOOGLE_TOKEN_PATH
    )
    print(f' Successful AutoParsing!')


schedule.every(parsing_time).minutes.do(autoparsing)

while True:
    schedule.run_pending()