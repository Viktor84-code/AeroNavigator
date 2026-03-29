"""Абстрактный базовый класс для работы с хранилищем данных."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseStorage(ABC):
    """Абстрактный базовый класс для работы с хранилищем данных."""

    @abstractmethod
    def add(self, item: Any) -> None:
        """
        Добавить элемент в хранилище.

        Args:
            item: Элемент для добавления (например, объект Aeroplane).
        """
        pass

    @abstractmethod
    def get(self, **criteria) -> List[Dict[str, Any]]:
        """
        Получить данные из хранилища по критериям.

        Args:
            **criteria: Ключевые слова для фильтрации (например, country="Russia").

        Returns:
            List[Dict[str, Any]]: Список словарей с данными.
        """
        pass

    @abstractmethod
    def delete(self, **criteria) -> int:
        """
        Удалить данные из хранилища по критериям.

        Args:
            **criteria: Ключевые слова для фильтрации.

        Returns:
            int: Количество удалённых записей.
        """
        pass
