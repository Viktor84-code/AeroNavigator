from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAPI(ABC):
    """Абстрактный базовый класс для работы с внешними API."""

    def __init__(self, base_url: str) -> None:
        """
        Инициализация с базовым URL.

        Args:
            base_url: Базовый адрес API
        """
        self._base_url = base_url

    @abstractmethod
    def _connect(self) -> bool:
        """
        Приватный метод для проверки подключения к API.

        Returns:
            bool: True, если подключение успешно
        """
        pass

    @abstractmethod
    def get_data(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Получение данных из API.

        Args:
            params: Параметры запроса

        Returns:
            List[Dict[str, Any]]: Список полученных данных
        """
        pass
