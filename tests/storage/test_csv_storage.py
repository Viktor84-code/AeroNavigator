"""
Тесты для класса CSVStorage.

Проверяют базовую функциональность: добавление, получение, удаление данных.
"""

from models.aeroplane import Aeroplane
from storage.csv_storage import CSVStorage


class TestCSVStorage:
    def test_add_and_get(self, tmp_path):
        file = tmp_path / "test.csv"
        storage = CSVStorage(filename=str(file))
        plane = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        storage.add(plane)
        data = storage.get()
        assert len(data) == 1
        assert data[0]["icao24"] == "abc123"

    def test_no_duplicates(self, tmp_path):
        file = tmp_path / "test.csv"
        storage = CSVStorage(filename=str(file))
        plane = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        storage.add(plane)
        storage.add(plane)  # дубликат
        data = storage.get()
        assert len(data) == 1

    def test_delete(self, tmp_path):
        file = tmp_path / "test.csv"
        storage = CSVStorage(filename=str(file))
        plane = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        storage.add(plane)
        deleted = storage.delete(country="Russia")
        assert deleted == 1
        data = storage.get()
        assert len(data) == 0

    def test_get_with_criteria(self, tmp_path):
        file = tmp_path / "test.csv"
        storage = CSVStorage(filename=str(file))
        plane1 = Aeroplane("abc123", "AFL123", "Russia", 10000.0, 850.0)
        plane2 = Aeroplane("def456", "UAL456", "USA", 12000.0, 900.0)
        storage.add_aeroplanes([plane1, plane2])
        result = storage.get(country="Russia")
        assert len(result) == 1
        assert result[0]["icao24"] == "abc123"
