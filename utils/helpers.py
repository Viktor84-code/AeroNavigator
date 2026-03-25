"""
Вспомогательные функции для фильтрации и сортировки самолётов.
"""

from typing import List
from models.aeroplane import Aeroplane


def filter_by_country(aeroplanes: List[Aeroplane], countries: List[str]) -> List[Aeroplane]:
    """Фильтрует самолёты по списку стран регистрации."""
    return [p for p in aeroplanes if p.country in countries]


def filter_by_altitude(aeroplanes: List[Aeroplane], min_alt: float, max_alt: float) -> List[Aeroplane]:
    """Фильтрует самолёты по диапазону высот."""
    return [p for p in aeroplanes if min_alt <= p.altitude <= max_alt]


def sort_by_altitude(aeroplanes: List[Aeroplane], reverse: bool = True) -> List[Aeroplane]:
    """Сортирует самолёты по высоте (по убыванию по умолчанию)."""
    return sorted(aeroplanes, key=lambda p: p.altitude, reverse=reverse)


def get_top_n(aeroplanes: List[Aeroplane], n: int) -> List[Aeroplane]:
    """Возвращает первые N самолётов из отсортированного списка."""
    return aeroplanes[:n]


def print_aeroplanes(aeroplanes: List[Aeroplane], title: str = "") -> None:
    """Выводит список самолётов в читаемом формате."""
    if title:
        print(f"\n📋 {title}")
    if not aeroplanes:
        print("Нет самолётов, соответствующих критериям.")
        return
    for plane in aeroplanes:
        print(f"  {plane.callsign} | {plane.country} | высота: {plane.altitude:.0f} м | скорость: {plane.velocity:.0f} м/с")
