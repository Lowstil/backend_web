"""
Задание 2. Информация по категории

Реализован Endpoint:
GET /categories/{category_id}
Возвращает информацию о конкретной категории услуг или 404, если категория не найдена.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from models import Category
import json

app = FastAPI(title="Задание 2: Информация по категории")

CATEGORIES = [
    {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
    {"id": 2, "name": "Маникюр и педикюр", "servicesCount": 5},
    {"id": 3, "name": "Брови и ресницы", "servicesCount": 4},
    {"id": 4, "name": "Спа-процедуры", "servicesCount": 4},
]


@app.get("/categories/{category_id}", response_model=Category)
def get_category_by_id(category_id: int):
    for category in CATEGORIES:
        if category["id"] == category_id:
            return category
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )


if __name__ == "__main__":
    print("=== Проверка Задания 2: GET /categories/{category_id} ===")
    client = TestClient(app)

    # 1. Запрос существующей категории (id=1)
    print("\n1. GET /categories/1 (Успешный запрос, 200):")
    res_200 = client.get("/categories/1")
    print(f"Статус-код: {res_200.status_code}")
    print("Тело ответа:")
    print(json.dumps(res_200.json(), ensure_ascii=False, indent=2))

    # 2. Запрос несуществующей категории (id=999)
    print("\n2. GET /categories/999 (Несуществующая категория, 404):")
    res_404 = client.get("/categories/999")
    print(f"Статус-код: {res_404.status_code}")
    print("Тело ответа:")
    print(res_404.json())
