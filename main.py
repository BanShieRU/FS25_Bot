from core.bot_initializer import bot
from config import DISCORD_TOKEN
import handlers.server_handlers

if __name__ == "__main__":
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("ОШИБКА: Отсутствует DISCORD_TOKEN")
        print("Создайте .env файл с содержанием:")
        print("DISCORD_TOKEN=ваш_токен_бота")
        print("API_URL=ваш_url_api_сервера")