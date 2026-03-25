#!/usr/bin/env python
"""
Точка входа в программу мониторинга самолетов
Запускаем интерактивный CLI-интерфейс для работы с API OpenSky и Nominatim.
"""


import sys
from typing import List, Optional
from api.aeroplanes_api import AeroplanesAPI
from models.aeroplane import Aeroplane
# from src.storage.json_storage import JSONStorage
# from src.utils.helpers import (
#     filter_by_country,
#     filter_by_altitude,
#     sort_by_altitude,
#     get_top_n,
#     print_aeroplanes
# )


def user_interaction() -> None:
    """
    Интерактивный CLI-интерфейс для работы с программой.

    Позволяет:
    - выбрать страну для мониторинга
    -получить топ N самолетов по высоте
    - отфильтровать самолеты по стране регистрации
    - отфильтровать по диапазону высот
    """

    print("\n✈️ Добро пожаловать в AeroNavigator!\n")

    # Шаг 1: создаём экземпляры классов (пока заглушки)
    api = AeroplanesAPI()
    storage = JSONStorage("data/flights.json")

    # Шаг 2: запрос страны
    country = input("🌍 Введите название страны (на английском, например, 'Russia'): ").strip()
    if not country:
        print("❌ Название страны не может быть пустым.")
        return

    print(f"\n🔍 Получаем данные о самолётах в воздушном пространстве {country}...")

    # Шаг 3: получаем данные из API
    try:
        aeroplanes_data = api.get_aeroplanes(country)
        if not aeroplanes_data:
            print("⚠️  Данные не получены. Возможно, API временно недоступно или страна не найдена.")
            return
        aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")
        return

    # Пока заглушка
    print("📡 (Заглушка) Данные получены. Сохраняем в JSON...")
    # storage.add_aeroplanes(aeroplanes)
    print("✅ Данные сохранены.")

    # Шаг 4: работа с пользовательскими фильтрами
    print("\n📊 Доступные действия:")
    print("1. Вывести топ N самолётов по высоте")
    print("2. Фильтр по стране регистрации")
    print("3. Фильтр по диапазону высот")
    print("4. Выйти")

    while True:
        choice = input("\nВыберите действие (1-4): ").strip()
        if choice == "4":
            print("👋 До свидания!")
            break
        elif choice == "1":
            # Топ N
            pass
        elif choice == "2":
            # Фильтр по стране
            pass
        elif choice == "3":
            # Фильтр по высоте
            pass
        else:
            print("❌ Неверный ввод. Попробуйте снова.")


def main() -> None:
    """Основная функция программы."""
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
