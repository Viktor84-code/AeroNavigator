import pytest

from models.aeroplane import Aeroplane
from utils.helpers import filter_by_altitude, filter_by_country, get_top_n, sort_by_altitude


@pytest.fixture
def sample_planes():
    """Тестовая эскадрилья для проверки фильтров."""
    return [
        Aeroplane("abc1", "AFL123", "Russia", 10000.0, 800.0),
        Aeroplane("def2", "LOT456", "Poland", 5000.0, 400.0),
        Aeroplane("ghi3", "N45", "USA", 12000.0, 900.0),
    ]


def test_filter_by_country(sample_planes):
    """Проверка фильтра по странам."""
    result = filter_by_country(sample_planes, ["Russia"])
    assert len(result) == 1
    assert result[0].callsign == "AFL123"


def test_filter_by_altitude(sample_planes):
    """Проверка фильтра по высоте."""
    result = filter_by_altitude(sample_planes, 4000, 6000)
    assert len(result) == 1
    assert result[0].country == "Poland"


def test_sort_by_altitude(sample_planes):
    """Проверка сортировки по убыванию."""
    result = sort_by_altitude(sample_planes)
    assert result[0].altitude == 12000.0


def test_get_top_n(sample_planes):
    """Проверка среза топ-N."""
    result = get_top_n(sample_planes, 2)
    assert len(result) == 2


def test_print_aeroplanes(capsys, sample_planes):
    """Проверка вывода списка самолётов (покрываем функцию print_aeroplanes)."""
    from utils.helpers import print_aeroplanes

    # 1. Тестируем вывод с заголовком и данными
    print_aeroplanes(sample_planes, title="Тестовый полет")
    out, err = capsys.readouterr()  # Перехватываем то, что ушло в консоль
    assert "Тестовый полет" in out
    assert "AFL123" in out
    assert "высота: 10000 м" in out

    # 2. Тестируем случай, когда список пустой (ветка 'if not aeroplanes')
    print_aeroplanes([], title="Пустой список")
    out, err = capsys.readouterr()
    assert "Нет самолётов, соответствующих критериям" in out
