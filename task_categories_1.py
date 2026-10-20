"""
Задание 1. Список категорий

Сгруппируем услуги по категориям. Реализован Endpoint:
GET /categories
Возвращает список всех категорий услуг с количеством услуг (servicesCount) в каждой.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from models import Category
import json

app = FastAPI(title="Задание 1: Список категорий")

CATEGORIES = [
    {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
    {"id": 2, "name": "Маникюр и педикюр", "servicesCount": 5},
    {"id": 3, "name": "Брови и ресницы", "servicesCount": 4},
    {"id": 4, "name": "Спа-процедуры", "servicesCount": 4},
]


@app.get("/categories", response_model=list[Category])
def get_categories():
    return CATEGORIES


if __name__ == "__main__":
    print("=== Проверка Задания 1: GET /categories ===")
    client = TestClient(app)
    response = client.get("/categories")

    print(f"Статус-код: {response.status_code}")
    print("Тело ответа:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
