import discord
import hashlib

PLAYER_COLORS = [
    0xFF5733, 0x33FF57, 0x3357FF, 0xF333FF,
    0xFF33A1, 0x33FFF3, 0xF3FF33, 0x8C33FF,
    0xFF8C33, 0x33FF8C, 0x338CFF, 0xFF33F3,
    0x33F3FF, 0xF3FF8C, 0x8CFF33, 0xFF338C
]

def get_player_color(player_name):
    hash_val = int(hashlib.md5(player_name.encode()).hexdigest()[:8], 16)
    return PLAYER_COLORS[hash_val % len(PLAYER_COLORS)]

def plural_mods(count):
    """Склоняет слово 'мод' в зависимости от числа"""
    if count % 10 == 1 and count % 100 != 11:
        return "мод"
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return "мода"
    else:
        return "модов"

def create_server_embed(status, map_name, map_size, mods_count, player_count):
    embed = discord.Embed(title="Статус сервера Farming Simulator 25", color=0x00ff00)
    
    if status == "Online":
        embed.color = 0x00ff00
        embed.description = "🟢 Сервер работает и доступен"
    elif status == "Standby":
        embed.color = 0xffa500
        embed.description = "🟠 Сервер остановлен, вебинтерфейс активен"
    else:
        embed.color = 0xff0000
        embed.description = "🔴 Сервер недоступен"
    
    if map_name != "Unknown":
        embed.add_field(name="Карта", value=f"{map_name} ({map_size}x{map_size})", inline=False)
    
    if mods_count > 0:
        mods_text = f"Установлено {mods_count} {plural_mods(mods_count)}"
        embed.add_field(name="Моды", value=mods_text, inline=False) 
 
    embed.add_field(name="Игроки онлайн", value=f"{player_count}/16", inline=False)
    
    status_info = {
        "Online": "Работает",
        "Standby": "Остановлен (вебинтерфейс активен)",
        "Offline": "Недоступен"
    }
    embed.add_field(name="Статус", value=status_info.get(status, "Неизвестно"), inline=False)
    
    embed.set_footer(text="Обновлено")
    return embed

def create_player_embed(player_name):
    color = get_player_color(player_name)
    return discord.Embed(description=f"👤 **{player_name}** в игре", color=color)