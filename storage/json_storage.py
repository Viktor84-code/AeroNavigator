import json
from typing import List

from models.aeroplane import Aeroplane
from utils.logger_config import logger


class JSONStorage:
    def __init__(self, filename: str = "data/flights.json"):
        self._filename = filename

    def add_aeroplanes(self, aeroplanes: List[Aeroplane]) -> None:
        """Сохраняет самолёты в JSON-файл (без дубликатов)."""
        existing = self._load()
        existing_icao = {a["icao24"] for a in existing}

        added_count = 0  # Счетчик для отчета

        for a in aeroplanes:
            if a.icao24 not in existing_icao:
                existing.append(
                    {
                        "icao24": a.icao24,
                        "callsign": a.callsign,
                        "country": a.country,
                        "altitude": a.altitude,
                        "velocity": a.velocity,
                    }
                )
                existing_icao.add(a.icao24)
                added_count += 1

        # Запись в файл
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        logger.info(f"Обновление БД: добавлено {added_count} новых бортов в {self._filename}")

    def _load(self) -> List[dict]:
        """Загружает данные из файла."""
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get(self, **criteria) -> List[dict]:
        """
        Получить данные из файла по критериям.

        Критерии могут быть: country, altitude_min, altitude_max, velocity_min, velocity_max
        """
        data = self._load()
        if not criteria:
            return data

        result = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if key == "country":
                    if item.get("country") != value:
                        match = False
                elif key == "altitude_min":
                    if item.get("altitude", 0) < value:
                        match = False
                elif key == "altitude_max":
                    if item.get("altitude", 0) > value:
                        match = False
                elif key == "velocity_min":
                    if item.get("velocity", 0) < value:
                        match = False
                elif key == "velocity_max":
                    if item.get("velocity", 0) > value:
                        match = False
                else:
                    if item.get(key) != value:
                        match = False
            if match:
                result.append(item)
        return result

    def delete(self, **criteria) -> int:
        """
        Удалить данные из файла по критериям.
        Возвращает количество удалённых записей.
        """
        data = self._load()
        if not criteria:
            return 0

        new_data = []
        removed = 0
        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                removed += 1
            else:
                new_data.append(item)

        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        return removed
