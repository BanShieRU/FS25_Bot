import discord
from services import fs25_service
from utils import formatters

async def update_player_messages(bot, text_channel, current_players):
    state = bot.server_state
    
    for player_name in list(state["player_messages"].keys()):
        if player_name not in current_players:
            try:
                message = await text_channel.fetch_message(state["player_messages"][player_name])
                await message.delete()
            except:
                pass
            finally:
                del state["player_messages"][player_name]
    
    for player_name in current_players:
        if player_name not in state["player_messages"]:
            try:
                embed = formatters.create_player_embed(player_name)
                message = await text_channel.send(embed=embed)
                state["player_messages"][player_name] = message.id
            except Exception as e:
                print(f"Ошибка создания сообщения игрока: {e}")

async def monitor_server(bot):
    current_players, status, map_name, map_size, mods_count = await fs25_service.fetch_server_data(bot.api_url)
    player_count = len(current_players)
    state = bot.server_state
    text_channel = bot.get_channel(bot.text_channel_id)
    
    if not text_channel:
        print("Ошибка: текстовый канал не найден!")
        return
    
    status_changed = status != state["status"]
    map_changed = map_name != state["map_name"]
    mods_changed = mods_count != state["mods_count"]
    players_changed = current_players != state["players"]
    
    if not any([status_changed, map_changed, mods_changed, players_changed]):
        return
       
    try:
        embed = formatters.create_server_embed(status, map_name, map_size, mods_count, player_count)
        
        if bot.status_message:
            try:
                await bot.status_message.edit(embed=embed)
            except discord.NotFound:
                bot.status_message = None
            except discord.HTTPException as e:
                print(f"Ошибка обновления сообщения: {e}")
                bot.status_message = None
        
        if not bot.status_message:
            bot.status_message = await text_channel.send(embed=embed)
    
    except Exception as e:
        print(f"Ошибка обновления статуса: {e}")

    if status == "Online" and players_changed:
        await update_player_messages(bot, text_channel, current_players)
    
    state.update({
        "status": status,
        "map_name": map_name,
        "map_size": map_size,
        "mods_count": mods_count,
        "players": current_players if status == "Online" else set()
    })