import requests
from typing import Dict, Any, List, Optional, Tuple
from utils.logger_config import logger  # ПОДКЛЮЧАЕМ НАШ САМОПИСЕЦ


class AeroplanesAPI:
    def __init__(self, user_agent: str = "AeroNavigator/1.0 (viktor84.code@gmail.com)"):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.user_agent = user_agent

    def get_country_coordinates(self, country: str) -> Optional[Tuple[float, float]]:
        logger.info(f"🌍 Поиск координат для страны: {country}")
        params = {"q": country, "format": "json", "limit": 1}
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(self.nominatim_url, params=params, headers=headers)
            if response.status_code != 200:
                logger.warning(f"⚠️ Ошибка Nominatim: Код {response.status_code}")
                return None
            data = response.json()
            if not data:
                logger.warning(f"❓ Страна '{country}' не найдена в базе Nominatim")
                return None

            lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
            logger.debug(f"📍 Координаты найдены: {lat}, {lon}")
            return (lat, lon)

        except (requests.RequestException, KeyError, ValueError, IndexError) as e:
            logger.error(f"❌ Критическая ошибка при поиске координат: {e}")
            return None

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        coords = self.get_country_coordinates(country)
        if not coords:
            return []

        lat, lon = coords
        logger.info(f"🛰️ Запрос самолетов в радиусе координат {lat}, {lon}")

        bbox = {
            "lamin": lat - 10,
            "lamax": lat + 10,
            "lomin": lon - 15,
            "lomax": lon + 15
        }
        try:
            response = requests.get(self.opensky_url, params=bbox, timeout=10)
            if response.status_code != 200:
                logger.error(f"❌ Ошибка OpenSky API: Код {response.status_code}")
                return []

            states = response.json().get("states", [])
            logger.info(f"✅ Получено бортов от OpenSky: {len(states) if states else 0}")
            return states if states else []

        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"❌ Ошибка при получении данных о полетах: {e}")
            return []
