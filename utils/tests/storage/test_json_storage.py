import pytest
import json
import os
from storage.json_storage import JSONStorage
from models.aeroplane import Aeroplane


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

    def test_get_by_country(self, temp_file):
        storage = JSONStorage(filename=str(temp_file))

        plane1 = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        plane2 = Aeroplane("def456", "UAL456", "USA", 12000.0, 900.0)
        storage.add_aeroplanes([plane1, plane2])

        result = storage.get(country="Russia")
        assert len(result) == 1
        assert result[0]["icao24"] == "abc123"

    def test_get_by_altitude_range(self, temp_file):
        storage = JSONStorage(filename=str(temp_file))

        plane1 = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        plane2 = Aeroplane("def456", "UAL456", "USA", 12000.0, 900.0)
        storage.add_aeroplanes([plane1, plane2])

        result = storage.get(altitude_min=11000, altitude_max=13000)
        assert len(result) == 1
        assert result[0]["icao24"] == "def456"

    def test_delete_by_country(self, temp_file):
        storage = JSONStorage(filename=str(temp_file))

        plane1 = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        plane2 = Aeroplane("def456", "UAL456", "USA", 12000.0, 900.0)
        storage.add_aeroplanes([plane1, plane2])

        deleted = storage.delete(country="Russia")
        assert deleted == 1

        remaining = storage.get()
        assert len(remaining) == 1
        assert remaining[0]["icao24"] == "def456"
