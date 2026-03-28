# mypy: ignore-errors
"""
Класс для работы с API Nominatim и OpenSky.

Реализует получение координат стран и данных о самолётах.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

import requests

from api.base_api import BaseAPI

logger = logging.getLogger(__name__)


class AeroplanesAPI(BaseAPI):
    """
    Класс для работы с API Nominatim и OpenSky.

    Позволяет получать координаты стран через Nominatim
    и данные о самолётах через OpenSky API.
    """

    def __init__(self, user_agent: str = "AeroNavigator/1.0 (viktor84.code@gmail.com)"):
        """
        Инициализация клиента API.

        Args:
            user_agent: Строка User-Agent для Nominatim API.
        """
        super().__init__(base_url="https://nominatim.openstreetmap.org/search")
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.user_agent = user_agent

    def _connect(self) -> bool:
        """
        Проверка подключения к OpenSky API.

        Returns:
            bool: True, если подключение успешно, иначе False.
        """
        try:
            response = requests.get(self.opensky_url, params={"lamin": 0, "lamax": 0}, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_data(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Получение данных по параметрам (например, по стране).

        Args:
            params: Словарь с параметрами запроса (должен содержать ключ "country").

        Returns:
            List[Dict[str, Any]]: Список данных о самолётах.
        """
        country = params.get("country")
        if not country:
            return []
        return self.get_aeroplanes(country)

    def get_country_coordinates(self, country: str) -> Optional[Tuple[float, float, float, float]]:
        """
        Получение boundingbox страны через Nominatim API.

        Returns:
            Optional[Tuple[float, float, float, float]]: (south, north, west, east)
        """
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

            bbox = data[0].get("boundingbox")
            if not bbox or len(bbox) != 4:
                logger.warning(f"❓ Некорректный boundingbox для '{country}'")
                return None

            south, north, west, east = map(float, bbox)
            logger.debug(f"📍 Boundingbox найден: {south}, {north}, {west}, {east}")
            return (south, north, west, east)

        except (requests.RequestException, KeyError, ValueError, IndexError) as e:
            logger.error(f"❌ Критическая ошибка при поиске координат: {e}")
            return None

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """
        Получение данных о самолётах в воздушном пространстве страны.

        Args:
            country: Название страны на английском.

        Returns:
            List[Dict[str, Any]]: Список данных о самолётах в формате OpenSky.
        """
        coords = self.get_country_coordinates(country)
        if not coords:
            return []

        south, north, west, east = coords
        bbox = {
            "lamin": south,
            "lamax": north,
            "lomin": west,
            "lomax": east,
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
