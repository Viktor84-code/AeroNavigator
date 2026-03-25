import requests
from typing import Dict, Any, List, Optional, Tuple


class AeroplanesAPI:
    def __init__(self, user_agent: str = "AeroNavigator/1.0 (viktor84.code@gmail.com)"):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.user_agent = user_agent

    def get_country_coordinates(self, country: str) -> Optional[Tuple[float, float]]:
        params = {"q": country, "format": "json", "limit": 1}
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(self.nominatim_url, params=params, headers=headers)
            if response.status_code != 200:
                return None
            data = response.json()
            if not data:
                return None
            return (float(data[0]["lat"]), float(data[0]["lon"]))
        except (requests.RequestException, KeyError, ValueError, IndexError):
            return None

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        coords = self.get_country_coordinates(country)
        if not coords:
            return []
        lat, lon = coords
        bbox = {
            "lamin": lat - 10,
            "lamax": lat + 10,
            "lomin": lon - 15,
            "lomax": lon + 15
        }
        try:
            response = requests.get(self.opensky_url, params=bbox, timeout=10)
            if response.status_code != 200:
                return []
            return response.json().get("states", [])
        except (requests.RequestException, KeyError, ValueError):
            return []
