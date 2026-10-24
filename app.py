"""
FastAPI приложение: реализация эндпоинтов категорий и мастеров салона красоты.
"""

from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import Category, Master, MasterSchema

app = FastAPI(
    title="Beauty Salon API",
    description="REST API для салона красоты: управление категориями услуг и мастерами (SQLAlchemy + SQLite)",
    version="3.0.0",
)


@app.on_event("startup")
def on_startup():
    """При старте приложения создаем таблицы и загружаем тестовые данные."""
    init_db()


# ==========================================================
# Эндпоинты мастеров (Задания: Модель Master и SQLite API)
# ==========================================================

@app.get(
    "/masters",
    response_model=List[MasterSchema],
    status_code=status.HTTP_200_OK,
    summary="Список мастеров",
    description="Возвращает список всех мастеров или мастеров указанной специализации из БД SQLite.",
    tags=["Мастера"],
)
def get_masters(
    specialization: Optional[str] = Query(
        None,
        description="Фильтрация мастеров по специализации (например: Парикмахер, Визажист)",
    ),
    db: Session = Depends(get_db),
):
    """
    Задание 2:
    1. GET /masters — получить список всех мастеров из таблицы базы данных.
    2. GET /masters?specialization=Парикмахер — получить только мастеров указанной специализации.
    """
    query = db.query(Master)
    if specialization:
        query = query.filter(Master.specialization == specialization)
    return query.all()


@app.get(
    "/masters/{master_id}",
    response_model=MasterSchema,
    status_code=status.HTTP_200_OK,
    summary="Информация о мастере",
    description="Возвращает информацию об одном мастере по его ID. Если мастер не найден — возвращает 404 Not Found.",
    responses={
        200: {
            "description": "Мастер успешно найден",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Анна",
                        "specialization": "Парикмахер",
                    }
                }
            },
        },
        404: {
            "description": "Мастер не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Master not found"}
                }
            },
        },
    },
    tags=["Мастера"],
)
def get_master_by_id(master_id: int, db: Session = Depends(get_db)):
    """
    Задание 2:
    3. GET /masters/{master_id} — получить одного мастера по его id из таблицы БД.
    """
    master = db.query(Master).filter(Master.id == master_id).first()
    if master is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found",
        )
    return master


# ==========================================================
# Эндпоинты категорий услуг (Из предыдущего задания)
# ==========================================================

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
    return CATEGORIES


@app.get(
    "/categories/{category_id}",
    response_model=Category,
    status_code=status.HTTP_200_OK,
    summary="Информация по категории",
    description="Возвращает информацию о конкретной категории услуг по её ID.",
    responses={
        200: {"description": "Категория найдена"},
        404: {"description": "Категория не найдена"},
    },
    tags=["Категории"],
)
def get_category_by_id(category_id: int):
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
            "GET /masters",
            "GET /masters?specialization={specialization}",
            "GET /masters/{master_id}",
            "GET /categories",
            "GET /categories/{category_id}",
        ],
    }
