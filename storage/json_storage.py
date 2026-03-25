import json
from typing import List
from models.aeroplane import Aeroplane


class JSONStorage:
    def __init__(self, filename: str = "data/flights.json"):
        self._filename = filename

    def add_aeroplanes(self, aeroplanes: List[Aeroplane]) -> None:
        """Сохраняет самолёты в JSON-файл (без дубликатов)."""
        existing = self._load()
        existing_icao = {a["icao24"] for a in existing}

        for a in aeroplanes:
            if a.icao24 not in existing_icao:
                existing.append({
                    "icao24": a.icao24,
                    "callsign": a.callsign,
                    "country": a.country,
                    "altitude": a.altitude,
                    "velocity": a.velocity
                })
                existing_icao.add(a.icao24)

        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

    def _load(self) -> List[dict]:
        """Загружает данные из файла."""
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
