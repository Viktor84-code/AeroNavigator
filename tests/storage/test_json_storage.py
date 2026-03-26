import json

import pytest

from models.aeroplane import Aeroplane
from storage.json_storage import JSONStorage


class TestJSONStorage:
    @pytest.fixture
    def temp_file(self, tmp_path):
        """Временный файл для тестов."""
        return tmp_path / "test_flights.json"

    def test_add_aeroplanes(self, temp_file):
        storage = JSONStorage(filename=str(temp_file))

        plane1 = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        plane2 = Aeroplane("def456", None, "USA", 12000.0, 900.0)

        storage.add_aeroplanes([plane1, plane2])

        with open(temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["icao24"] == "abc123"
        assert data[1]["callsign"] == "N/A"  # проверяем значение по умолчанию

    def test_no_duplicates(self, temp_file):
        storage = JSONStorage(filename=str(temp_file))

        plane = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        storage.add_aeroplanes([plane, plane])  # дважды добавляем один и тот же

        with open(temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1  # дубликат не должен добавиться

    def test_load_empty(self, temp_file):
        storage = JSONStorage(filename=str(temp_file))
        # Файла нет, должно загрузиться []
        data = storage._load()
        assert data == []

    def test_storage_get_with_criteria(self, temp_file):
        """Проверка фильтрации данных из файла (покрываем метод get)."""
        # 1. Создаем хранилище, используя твой временный файл
        from storage.json_storage import JSONStorage

        storage = JSONStorage(filename=str(temp_file))

        # 2. Забиваем тестовые данные
        planes = [
            Aeroplane("icao1", "AFL123", "Russia", 10000.0, 800.0),
            Aeroplane("icao2", "LOT456", "Poland", 5000.0, 400.0),
        ]
        storage.add_aeroplanes(planes)

        # 3. Проверка фильтра по стране
        result = storage.get(country="Russia")
        assert len(result) == 1
        assert result[0]["callsign"] == "AFL123"

        # 4. Проверка фильтра по высоте (мин/макс)
        result = storage.get(altitude_min=4000, altitude_max=6000)
        assert len(result) == 1
        assert result[0]["country"] == "Poland"

        # 5. Проверка без критериев (должен вернуть все 2 записи)
        result = storage.get()
        assert len(result) == 2

        # 6. Добиваем 'velocity_max' (ветка, которая была пустой)
        # Ищем самолеты со скоростью НЕ БОЛЬШЕ 500
        result = storage.get(velocity_max=500)
        assert len(result) == 1
        assert result[0]["icao24"] == "icao2"

        # 7. Добиваем финальный 'else' (универсальный фильтр по любому ключу)
        # Например, фильтр по конкретному icao24
        result = storage.get(icao24="icao1")
        assert len(result) == 1
        assert result[0]["callsign"] == "AFL123"

        # 8. Добиваем 'velocity_min' (на всякий случай, если пропустили)
        result = storage.get(velocity_min=600)
        assert len(result) == 1
        assert result[0]["icao24"] == "icao1"

    def test_storage_delete_with_criteria(self, temp_file):
        """Проверка удаления данных из файла (покрываем метод delete)."""
        # 1. Готовим хранилище и данные
        from storage.json_storage import JSONStorage

        storage = JSONStorage(filename=str(temp_file))

        planes = [
            Aeroplane("icao1", "AFL123", "Russia", 10000.0, 800.0),
            Aeroplane("icao2", "LOT456", "Poland", 5000.0, 400.0),
        ]
        storage.add_aeroplanes(planes)

        # 2. Удаляем по критерию (например, по позывному)
        removed_count = storage.delete(callsign="AFL123")

        # 3. Проверки: вернуло 1 удаление, в базе остался 1 самолет
        assert removed_count == 1
        data_after = storage._load()
        assert len(data_after) == 1
        assert data_after[0]["icao24"] == "icao2"

        # 4. Проверка удаления без критериев (должно вернуть 0 по твоей логике)
        assert storage.delete() == 0
