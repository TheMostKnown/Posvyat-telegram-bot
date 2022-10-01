import django
import os
import logging
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from tgbot.handlers.spreadsheet_parser.commands.export_to_db import get_init_data
from tgbot.handlers.dispatcher import run_pooling, bot
from dtb.settings import GOOGLE_TABLE_ID, GOOGLE_TOKEN_PATH, GOOGLE_CREDS_PATH

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(GOOGLE_CREDS_PATH)
    get_init_data(
        spreadsheet_id=GOOGLE_TABLE_ID,
        creds_file_name=GOOGLE_CREDS_PATH,
        token_file_name=GOOGLE_TOKEN_PATH,
        bot = bot
    )
    print(f"Launching bot at {datetime.now().time().strftime('%H:%M')}")
    run_pooling()
