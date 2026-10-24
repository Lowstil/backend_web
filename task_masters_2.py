"""
Задание 2. Реализуйте API

Реализованы API-методы для получения информации по мастерам из SQLite БД:
1. GET /masters — получить список всех мастеров из таблицы базы данных.
2. GET /masters?specialization=Парикмахер — получить только мастеров указанной специализации.
3. GET /masters/{master_id} — получить одного мастера по его id из таблицы БД (404 Not Found если не найден).
"""

import json
from fastapi.testclient import TestClient

from app import app
from database import init_db

if __name__ == "__main__":
    init_db()
    client = TestClient(app)

    print("=== Проверка Задания 2: API методы для мастеров ===")

    # 1. GET /masters
    print("\n1. GET /masters (Список всех мастеров):")
    res1 = client.get("/masters")
    print(f"Статус-код: {res1.status_code}")
    print("Тело ответа:")
    print(json.dumps(res1.json(), ensure_ascii=False, indent=2))

    # 2. GET /masters?specialization=Парикмахер
    print("\n2. GET /masters?specialization=Парикмахер (Фильтрация по специализации):")
    res2 = client.get("/masters", params={"specialization": "Парикмахер"})
    print(f"Статус-код: {res2.status_code}")
    print("Тело ответа:")
    print(json.dumps(res2.json(), ensure_ascii=False, indent=2))

    # 3. GET /masters/1
    print("\n3. GET /masters/1 (Получение мастера по id):")
    res3 = client.get("/masters/1")
    print(f"Статус-код: {res3.status_code}")
    print("Тело ответа:")
    print(json.dumps(res3.json(), ensure_ascii=False, indent=2))

    # 4. GET /masters/999 (Несуществующий мастер)
    print("\n4. GET /masters/999 (Мастер не найден):")
    res4 = client.get("/masters/999")
    print(f"Статус-код: {res4.status_code}")
    print("Тело ответа:")
    print(res4.json())
