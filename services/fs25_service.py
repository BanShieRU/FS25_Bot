import requests
import xml.etree.ElementTree as ET

async def fetch_server_data(api_url):
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        if 'game' in root.attrib:
            players = set()
            map_name = root.get('mapName', 'Unknown')
            map_size = root.get('mapSize', 'Unknown')
            mods_count = len(root.findall('.//Mods/Mod'))
            
            for player in root.findall('.//Slots/Player'):
                if player.get('isUsed') == 'true':
                    player_name = player.text.strip() if player.text else "Unknown"
                    players.add(player_name)
            
            return players, "Online", map_name, map_size, mods_count
        
        elif root.find('.//Slots') is not None:
            return set(), "Standby", "Unknown", "Unknown", 0
        
        else:
            return set(), "Offline", "Unknown", "Unknown", 0
            
    except (requests.exceptions.RequestException, ET.ParseError):
        return set(), "Offline", "Unknown", "Unknown", 0
    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return set(), "Offline", "Unknown", "Unknown", 0