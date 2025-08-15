import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL', 'http://5.188.9.175:8081/feed/dedicated-server-stats.xml?code=3937c4252a2f9b489690c84d82a14c80')
TEXT_CHANNEL_ID = int(os.getenv('TEXT_CHANNEL_ID', 1337088418580004925))
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 10))