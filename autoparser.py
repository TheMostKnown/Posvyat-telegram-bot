import django
import os
import logging
import schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from tgbot.handlers.spreadsheet_parser.commands.export_to_db import get_init_data
from dtb.settings import GOOGLE_TABLE_ID, GOOGLE_TOKEN_PATH, GOOGLE_CREDS_PATH


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.info('Initialize autoparser')


def autoparsing():
    logger.info(GOOGLE_CREDS_PATH)
    logger.info('AUTOPARSING!')
    get_init_data(
        spreadsheet_id=GOOGLE_TABLE_ID,
        creds_file_name=GOOGLE_CREDS_PATH,
        token_file_name=GOOGLE_TOKEN_PATH
    )
    logger.info(f' Successfull AutoParsing ')


schedule.every(1).minutes.do(autoparsing)

while True:
    schedule.run_pending()
    