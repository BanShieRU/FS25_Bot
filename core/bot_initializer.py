import discord
from discord.ext import tasks
from config import DISCORD_TOKEN, TEXT_CHANNEL_ID, CHECK_INTERVAL, API_URL

class FS25Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_state = {
            "status": "unknown",
            "map_name": "Unknown",
            "map_size": "Unknown",
            "mods_count": 0,
            "players": set(),
            "player_messages": {}
        }
        self.status_message = None
        self.text_channel_id = TEXT_CHANNEL_ID
        self.api_url = API_URL
        self.check_interval = CHECK_INTERVAL
        self.monitor_task = None

    async def start_monitoring(self):
        if not self.monitor_task or self.monitor_task.done():
            self.monitor_task = tasks.loop(seconds=self.check_interval)(self._monitor_server)
            self.monitor_task.start()

    async def _monitor_server(self):
        from services.monitor_service import monitor_server
        await monitor_server(self)

bot = FS25Bot(intents=discord.Intents.default())