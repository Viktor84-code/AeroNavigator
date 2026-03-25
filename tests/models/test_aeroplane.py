import pytest
from models.aeroplane import Aeroplane


class TestAeroplane:
    def test_create_aeroplane(self):
        """Создание объекта Aeroplane с корректными данными."""
        plane = Aeroplane(
            icao24="abc123",
            callsign="AFL123",
            country="Russia",
            altitude=10000.0,
            velocity=850.0
        )
        assert plane.icao24 == "abc123"
        assert plane.callsign == "AFL123"
        assert plane.country == "Russia"
        assert plane.altitude == 10000.0
        assert plane.velocity == 850.0

    def test_callsign_default(self):
        """Если позывной отсутствует, значение по умолчанию — 'N/A'."""
        plane = Aeroplane(
            icao24="abc123",
            callsign=None,
            country="Russia",
            altitude=10000.0,
            velocity=850.0
        )
        assert plane.callsign == "N/A"

    def test_altitude_default(self):
        """Если высота отсутствует, значение по умолчанию — 0.0."""
        plane = Aeroplane(
            icao24="abc123",
            callsign="AFL123",
            country="Russia",
            altitude=None,
            velocity=850.0
        )
        assert plane.altitude == 0.0

    def test_velocity_default(self):
        """Если скорость отсутствует, значение по умолчанию — 0.0."""
        plane = Aeroplane(
            icao24="abc123",
            callsign="AFL123",
            country="Russia",
            altitude=10000.0,
            velocity=None
        )
        assert plane.velocity == 0.0

    def test_cast_to_object_list(self):
        """Преобразование данных OpenSky в список объектов Aeroplane."""
        data = [
            ["abc123", "AFL123", "Russia", 0, 0, 0, 0, 10000.0, 0, 850.0],
            ["def456", None, "USA", 0, 0, 0, 0, 12000.0, 0, 900.0],
            ["short"]  # невалидный элемент
        ]
        planes = Aeroplane.cast_to_object_list(data)
        assert len(planes) == 2
        assert planes[0].icao24 == "abc123"
        assert planes[0].callsign == "AFL123"
        assert planes[0].altitude == 10000.0
        assert planes[1].callsign == "N/A"
