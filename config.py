from pytz import timezone
from dotenv import load_dotenv
from os import getenv

load_dotenv()


NY_TIMEZONE = timezone('US/Eastern')

BOT_TOKEN = getenv('BOT_TOKEN')
RECEIVER_ID = getenv('RECEIVER_ID')