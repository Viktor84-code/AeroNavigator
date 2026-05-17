"""
Класс для работы с CSV-файлом как хранилищем данных о самолётах.

Реализует методы add, get, delete для работы с самолётами в формате CSV.
"""

import csv
from typing import Any, Dict, List

from models.aeroplane import Aeroplane
from storage.base_storage import BaseStorage


class CSVStorage(BaseStorage):
    """Хранилище данных в CSV-файле.

    Реализует методы add, get, delete для работы с самолётами.
    """

    def __init__(self, filename: str = "data/flights.csv"):
        """Инициализация хранилища."""
        self._filename = filename

    def add(self, item: Aeroplane) -> None:
        """Добавляет один самолёт в CSV-файл (без дубликатов)."""
        data = self._load()
        for row in data:
            if row["icao24"] == item.icao24:
                return
        data.append(
            {
                "icao24": item.icao24,
                "callsign": item.callsign,
                "country": item.country,
                "altitude": item.altitude,
                "velocity": item.velocity,
            }
        )
        self._save(data)

    def add_aeroplanes(self, aeroplanes: List[Aeroplane]) -> None:
        """Добавляет список самолётов в CSV-файл (без дубликатов)."""
        data = self._load()
        existing_icao = {row["icao24"] for row in data}
        for a in aeroplanes:
            if a.icao24 not in existing_icao:
                data.append(
                    {
                        "icao24": a.icao24,
                        "callsign": a.callsign,
                        "country": a.country,
                        "altitude": a.altitude,
                        "velocity": a.velocity,
                    }
                )
                existing_icao.add(a.icao24)
        self._save(data)

    def get(self, **criteria) -> List[Dict[str, Any]]:
        """Получить данные из CSV-файла по критериям."""
        data = self._load()
        if not criteria:
            return data
        result = []
        for row in data:
            match = True
            for key, val in criteria.items():
                if row.get(key) != val:
                    match = False
                    break
            if match:
                result.append(row)
        return result

    def delete(self, **criteria) -> int:
        """Удалить данные из CSV-файла по критериям."""
        data = self._load()
        if not criteria:
            return 0
        new_data = []
        removed = 0
        for row in data:
            match = True
            for key, val in criteria.items():
                if row.get(key) != val:
                    match = False
                    break
            if match:
                removed += 1
            else:
                new_data.append(row)
        self._save(new_data)
        return removed

    def _load(self) -> List[dict]:
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except (FileNotFoundError, StopIteration):
            return []

    def _save(self, data: List[dict]) -> None:
        with open(self._filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["icao24", "callsign", "country", "altitude", "velocity"])
            writer.writeheader()
            writer.writerows(data)
