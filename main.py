#!/usr/bin/env python
"""
Точка входа в программу мониторинга самолетов
Запускаем интерактивный CLI-интерфейс для работы с API OpenSky и Nominatim.
"""

import sys

from api.aeroplanes_api import AeroplanesAPI
from models.aeroplane import Aeroplane
from storage.json_storage import JSONStorage
from utils.helpers import (
    filter_by_altitude,
    filter_by_country,
    get_top_n,
    print_aeroplanes,
    sort_by_altitude,
)
from utils.logger_config import logger


def user_interaction() -> None:
    """
    Интерактивный CLI-интерфейс для работы с программой.

    Позволяет:
    - выбрать страну для мониторинга
    - получить топ N самолетов по высоте
    - отфильтровать самолеты по стране регистрации
    - отфильтровать по диапазону высот
    """

    print("\n✈️ Добро пожаловать в AeroNavigator!\n")

    # Создаём экземпляры классов
    api = AeroplanesAPI()
    storage = JSONStorage("data/flights.json")

    # Запрос страны
    country = input("🌍 Введите название страны (на английском, например, 'Russia'): ").strip()
    if not country:
        print("❌ Название страны не может быть пустым.")
        return

    # ЛОГИРУЕМ СТАРТ
    logger.info(f"Запуск мониторинга для региона: {country}")

    # Получаем данные из API
    try:
        aeroplanes_data = api.get_aeroplanes(country)
        if not aeroplanes_data:
            logger.warning(f"Данные для '{country}' не получены.")
            print("⚠️ Ошибка: Данные не получены. Проверьте интернет или название страны.")
            return

        aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

        # 1. Собираем список стран, чтобы ТЫ их видел в консоли
        available_countries = sorted(list(set(p.country for p in aeroplanes)))

        # 2. Сохраняем в базу
        storage.add_aeroplanes(aeroplanes)
        logger.info(f"Успешно сохранено {len(aeroplanes)} бортов. Страны: {available_countries}")

        # 3. ВЫВОДИМ В КОНСОЛЬ ТО, ЧТО ТЕБЕ НУЖНО
        print(f"✅ Готово! В небе {country} обнаружено {len(aeroplanes)} самолетов.")
        print(f"🌍 Доступные страны для фильтрации: {', '.join(available_countries)}")

    except Exception as e:
        logger.error(f"Критический сбой в цикле получения данных: {e}", exc_info=True)
        print("❌ Системная ошибка. Подробности в logs/navigator.log")
        return

    # Работа с пользовательскими фильтрами
    while True:
        print("\n📊 Доступные действия:")
        print("1. Вывести топ N самолётов по высоте")
        print("2. Фильтр по стране регистрации")
        print("3. Фильтр по диапазону высот")
        print("4. Выйти")

        choice = input("\nВыберите действие (1-4): ").strip()

        if choice == "4":
            logger.info("Пользователь завершил работу с программой.")
            print("👋 До свидания!")
            break

        elif choice == "1":
            try:
                n = int(input("Введите количество самолётов для топа: "))
                sorted_planes = sort_by_altitude(aeroplanes)
                top_planes = get_top_n(sorted_planes, n)
                print_aeroplanes(top_planes, title=f"Топ {n} самолётов по высоте")
            except ValueError:
                print("❌ Введите целое число.")

        elif choice == "2":
            countries_input = input("Введите страны регистрации через запятую: ")
            countries = [c.strip() for c in countries_input.split(",")]
            filtered = filter_by_country(aeroplanes, countries)
            print_aeroplanes(filtered, title="Отфильтровано по стране регистрации")

        elif choice == "3":
            try:
                min_alt = int(input("Минимальная высота (м): "))
                max_alt = int(input("Максимальная высота (м): "))
                filtered = filter_by_altitude(aeroplanes, min_alt, max_alt)
                print_aeroplanes(filtered, title=f"Самолёты на высоте {min_alt}-{max_alt} м")
            except ValueError:
                print("❌ Введите целые числа.")
        else:
            print("❌ Неверный ввод. Попробуйте снова.")


def main() -> None:
    """Основная функция программы (точка входа)."""
    try:
        user_interaction()
    except KeyboardInterrupt:
        logger.warning("Программа прервана пользователем через Ctrl+C")
        print("\n\n👋 Программа прервана.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Непредвиденная системная ошибка в main: {e}", exc_info=True)
        print(f"\n❌ Непредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
