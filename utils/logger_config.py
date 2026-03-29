"""Настройка логирования для проекта."""

import logging
from pathlib import Path


def setup_logging():
    """Настройка логирования: файл и консоль."""
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "navigator.log"

    log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # 1. Создаем обработчик для ФАЙЛА (Пишем ВСЁ)
    file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
    file_handler.setLevel(logging.INFO)  # Сюда летит вся инфа
    file_handler.setFormatter(log_format)

    # 2. Создаем обработчик для КОНСОЛИ (Только важное)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)  # В консоль только Варнинги и Ошибки
    stream_handler.setFormatter(log_format)

    # Настраиваем главный логгер
    root_logger = logging.getLogger("AeroNavigator")
    root_logger.setLevel(logging.INFO)

    # Очищаем старые хвосты и добавляем новые правила
    root_logger.handlers = []
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    return root_logger


logger = setup_logging()
