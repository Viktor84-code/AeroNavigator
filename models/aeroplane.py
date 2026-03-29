"""
Модель воздушного судна.

Содержит класс Aeroplane с валидацией, магическими методами и оптимизацией памяти.
"""

from typing import Any, List, Optional

from utils.logger_config import logger


class Aeroplane:
    """
    Представление воздушного судна.

    Атрибуты:
        icao24 (str): Уникальный идентификатор транспондера.
        callsign (str): Позывной (бортовой номер). По умолчанию "N/A".
        country (str): Страна регистрации.
        altitude (float): Высота полёта в метрах.
        velocity (float): Скорость полёта в метрах в секунду.
    """

    __slots__ = ("_icao24", "_callsign", "_country", "_altitude", "_velocity")

    def __init__(
        self,
        icao24: str,
        callsign: Optional[str],
        country: str,
        altitude: Optional[float],
        velocity: Optional[float],
    ) -> None:
        """
        Инициализация объекта самолёта.

        Args:
            icao24: Уникальный идентификатор.
            callsign: Позывной (может быть None).
            country: Страна регистрации.
            altitude: Высота (может быть None).
            velocity: Скорость (может быть None).
        """
        self._icao24 = icao24
        self._callsign = callsign if callsign is not None else "N/A"
        self._country = country
        self._altitude = self._validate_altitude(altitude)
        self._velocity = self._validate_velocity(velocity)

    # Геттеры
    @property
    def icao24(self) -> str:
        """Возвращает уникальный идентификатор."""
        return self._icao24

    @property
    def callsign(self) -> str:
        """Возвращает позывной."""
        return self._callsign

    @property
    def country(self) -> str:
        """Возвращает страну регистрации."""
        return self._country

    @property
    def altitude(self) -> float:
        """Возвращает высоту полёта."""
        return self._altitude

    @property
    def velocity(self) -> float:
        """Возвращает скорость полёта."""
        return self._velocity

    # Приватные методы валидации
    @staticmethod
    def _validate_altitude(value: Optional[float]) -> float:
        """Валидирует высоту: None или отрицательное значение заменяет на 0.0."""
        if value is None or value < 0:
            return 0.0
        return float(value)

    @staticmethod
    def _validate_velocity(value: Optional[float]) -> float:
        """Валидирует скорость: None или отрицательное значение заменяет на 0.0."""
        if value is None or value < 0:
            return 0.0
        return float(value)

    # Магические методы сравнения
    def __lt__(self, other: "Aeroplane") -> bool:
        """Сравнивает самолёты по высоте (меньше)."""
        return self._altitude < other._altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """Сравнивает самолёты по высоте (больше)."""
        return self._altitude > other._altitude

    def __eq__(self, other: object) -> bool:
        """Сравнивает самолёты по высоте (равно)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._altitude == other._altitude

    @classmethod
    def cast_to_object_list(cls, data: List[Any]) -> List["Aeroplane"]:
        """
        Преобразует данные OpenSky в список объектов Aeroplane.

        Args:
            data: Список списков с данными от OpenSky API.

        Returns:
            List[Aeroplane]: Список объектов самолётов.
        """
        aeroplanes = []
        for item in data:
            if len(item) >= 10:
                aeroplanes.append(
                    cls(
                        icao24=item[0],
                        callsign=item[1],
                        country=item[2],
                        altitude=item[13] if len(item) > 13 and item[13] is not None else item[7],
                        velocity=item[9],
                    )
                )

        logger.debug(f"Моделирование: создано {len(aeroplanes)} объектов из сырых данных")
        return aeroplanes
