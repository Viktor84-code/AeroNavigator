"""Класс для работы с JSON-файлом как хранилищем данных о самолётах."""

import json
from typing import Any, Dict, List

from models.aeroplane import Aeroplane
from storage.base_storage import BaseStorage
from utils.logger_config import logger


class JSONStorage(BaseStorage):
    """
    Хранилище данных в JSON-файле.

    Реализует методы add, get, delete для работы с самолётами.
    """

    def __init__(self, filename: str = "data/flights.json"):
        """
        Инициализация хранилища.

        Args:
            filename: Путь к JSON-файлу.
        """
        self._filename = filename

    def add(self, item: Aeroplane) -> None:
        """
        Добавляет один самолёт в хранилище (без дубликатов).

        Args:
            item: Объект Aeroplane.
        """
        existing = self._load()
        existing_icao = {a["icao24"] for a in existing}

        if item.icao24 not in existing_icao:
            existing.append(
                {
                    "icao24": item.icao24,
                    "callsign": item.callsign,
                    "country": item.country,
                    "altitude": item.altitude,
                    "velocity": item.velocity,
                }
            )
            self._save(existing)
            logger.info(f"✅ Добавлен самолёт {item.callsign} в {self._filename}")

    def add_aeroplanes(self, aeroplanes: List[Aeroplane]) -> None:
        """
        Добавляет список самолётов в хранилище (без дубликатов).

        Args:
            aeroplanes: Список объектов Aeroplane.
        """
        existing = self._load()
        existing_icao = {a["icao24"] for a in existing}

        added_count = 0
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

        self._save(existing)
        logger.info(f"Обновление БД: добавлено {added_count} новых бортов в {self._filename}")

    def get(self, **criteria) -> List[Dict[str, Any]]:
        """
        Получить данные из файла по критериям.

        Критерии могут быть: country, altitude_min, altitude_max, velocity_min, velocity_max.

        Returns:
            List[Dict[str, Any]]: Список словарей с данными самолётов.
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

        Returns:
            int: Количество удалённых записей.
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

        self._save(new_data)
        logger.info(f"🗑️ Удалено {removed} записей из {self._filename}")
        return removed

    def _load(self) -> List[dict]:
        """Загружает данные из файла."""
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, data: List[dict]) -> None:
        """Сохраняет данные в файл."""
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
