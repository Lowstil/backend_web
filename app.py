"""
FastAPI приложение: реализация эндпоинтов категорий услуг салона красоты.
"""

from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import Category

app = FastAPI(
    title="Beauty Salon API",
    description="REST API для салона красоты: управление категориями услуг и записями клиентов",
    version="2.0.0",
)

# Исходные данные категорий услуг согласно заданию
CATEGORIES: list[dict] = [
    {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
    {"id": 2, "name": "Маникюр и педикюр", "servicesCount": 5},
    {"id": 3, "name": "Брови и ресницы", "servicesCount": 4},
    {"id": 4, "name": "Спа-процедуры", "servicesCount": 4},
]


@app.get(
    "/categories",
    response_model=List[Category],
    status_code=status.HTTP_200_OK,
    summary="Список категорий",
    description="Возвращает список всех категорий услуг с количеством услуг (servicesCount) в каждой.",
    tags=["Категории"],
)
def get_categories():
    """
    Задание 1. Список категорий.
    GET /categories
    """
    return CATEGORIES


@app.get(
    "/categories/{category_id}",
    response_model=Category,
    status_code=status.HTTP_200_OK,
    summary="Информация по категории",
    description="Возвращает информацию о конкретной категории услуг по её идентификатору.",
    responses={
        200: {
            "description": "Категория успешно найдена",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Стрижки и укладки",
                        "servicesCount": 5,
                    }
                }
            },
        },
        404: {
            "description": "Категория не найдена",
            "content": {
                "application/json": {
                    "example": {"detail": "Category not found"}
                }
            },
        },
    },
    tags=["Категории"],
)
def get_category_by_id(category_id: int):
    """
    Задание 2. Информация по категории.
    GET /categories/{category_id}
    """
    for category in CATEGORIES:
        if category["id"] == category_id:
            return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )


@app.get("/", tags=["Справка"])
def root():
    return {
        "message": "Beauty Salon API is running",
        "documentation": "/docs",
        "endpoints": [
            "GET /categories",
            "GET /categories/{category_id}",
        ],
    }
