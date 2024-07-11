import os
from dotenv import load_dotenv

load_dotenv()

API_URL= os.getenv('API_URL')
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
DATABASE_FILE = os.getenv('DATABASE_FILE')
EMBED_NAME = os.getenv('EMBED_NAME')
EMBED_URL = os.getenv('EMBED_URL')
EMBED_ICON_URL = os.getenv('EMBED_ICON_URL')
EMBED_THUMBNAIL_URL = os.getenv('EMBED_THUMBNAIL_URL')
