"""
Задание 1. Pydantic-модель ServiceCreate

Модель содержит минимум 5 полей:
- categoryId
- title (не пустое, макс 100 символов)
- desc (не пустое, макс 100 символов)
- duration (от 30 мин до 180 мин / 3 часов)
- price (строго > 0)
"""

import json
from pydantic import ValidationError
from models import ServiceCreate


def test_service_create_validation():
    print("=== Проверка Задания 1: Pydantic-модель ServiceCreate ===")

    # 1. Корректные данные
    print("\n1. Проверка корректных данных:")
    valid_data = {
        "categoryId": 3,
        "title": "Наращивание ресниц",
        "desc": "Огромные ресницы уже через 30 минут",
        "duration": 30,
        "price": 1500.00,
    }
    try:
        service = ServiceCreate(**valid_data)
        print(" Успешная валидация:")
        print(json.dumps(service.model_dump(), ensure_ascii=False, indent=2))
    except ValidationError as e:
        print(" Ошибка:", e)

    # 2. Некорректная цена: 'бесплатно'
    print("\n2. Проверка некорректного типа цены ('бесплатно'):")
    invalid_price_data = {
        "categoryId": 3,
        "title": "Наращивание ресниц",
        "desc": "Огромные ресницы уже через 30 минут",
        "duration": 30,
        "price": "бесплатно",
    }
    try:
        ServiceCreate(**invalid_price_data)
        print(" Ошибка: данные не должны были пройти валидацию!")
    except ValidationError as e:
        print(" Ожидаемая ошибка валидации (422):")
        for err in e.errors():
            print(f"   - Поле '{err['loc'][0]}': {err['msg']}")

    # 3. Пустое описание, нулевая длительность, отрицательная цена
    print("\n3. Проверка пустого описания, duration=0, price=-1500.00:")
    invalid_data = {
        "categoryId": 3,
        "title": "Наращивание ресниц",
        "desc": "",
        "duration": 0,
        "price": -1500.00,
    }
    try:
        ServiceCreate(**invalid_data)
        print(" Ошибка: данные не должны были пройти валидацию!")
    except ValidationError as e:
        print(" Ожидаемая ошибка валидации (422):")
        for err in e.errors():
            print(f"   - Поле '{err['loc'][0]}': {err['msg']}")


if __name__ == "__main__":
    test_service_create_validation()
