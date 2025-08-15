from core.bot_initializer import bot

@bot.event
async def on_ready():
    print(f"Бот авторизован как {bot.user}")
    print("Начинаю мониторинг сервера...")
    await bot.start_monitoring()