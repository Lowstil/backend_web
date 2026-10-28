"""
Задание 2. Реализуйте API POST /services

Реализован эндпоинт POST /services с использованием Pydantic-модели ServiceCreate.
Добавление новой услуги в БД SQLite.
"""

import json
from fastapi.testclient import TestClient

from app import app
from database import SessionLocal, init_db
from models import Service

if __name__ == "__main__":
    init_db()
    client = TestClient(app)

    print("=== Проверка Задания 2: POST /services ===")

    # 1. Корректный запрос (201 Created)
    print("\n1. Запрос POST /services с корректными данными:")
    payload_1 = {
        "categoryId": 3,
        "title": "Наращивание ресниц",
        "desc": "Огромные ресницы уже через 30 минут",
        "duration": 30,
        "price": 1500.00,
    }
    res_1 = client.post("/services", json=payload_1)
    print(f"Статус-код: {res_1.status_code} (Ожидаем 201)")
    print("Тело ответа:")
    print(json.dumps(res_1.json(), ensure_ascii=False, indent=2))

    # 2. Некорректный запрос: price = 'бесплатно' (422)
    print("\n2. Запрос POST /services с ценой 'бесплатно':")
    payload_2 = {
        "categoryId": 3,
        "title": "Наращивание ресниц",
        "desc": "Огромные ресницы уже через 30 минут",
        "duration": 30,
        "price": "бесплатно",
    }
    res_2 = client.post("/services", json=payload_2)
    print(f"Статус-код: {res_2.status_code} (Ожидаем 422)")

    # 3. Некорректный запрос: desc = '', duration = 0, price = -1500.00 (422)
    print("\n3. Запрос POST /services с пустым описанием, duration=0, price=-1500.00:")
    payload_3 = {
        "categoryId": 3,
        "title": "Наращивание ресниц",
        "desc": "",
        "duration": 0,
        "price": -1500.00,
    }
    res_3 = client.post("/services", json=payload_3)
    print(f"Статус-код: {res_3.status_code} (Ожидаем 422)")

    # 4. Проверка сохранения в SQLite БД
    print("\n4. Проверка наличия услуги в таблице 'services' SQLite БД:")
    with SessionLocal() as db:
        saved_services = db.query(Service).filter(Service.title == "Наращивание ресниц").all()
        print(f"Найдено записей в БД: {len(saved_services)}")
        for s in saved_services:
            print(f" - ID: {s.id}, categoryId: {s.category_id}, title: '{s.title}', duration: {s.duration} мин, price: {s.price} руб.")
