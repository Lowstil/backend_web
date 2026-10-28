"""
FastAPI приложение: реализация эндпоинтов категорий, мастеров и услуг салона красоты.
"""

from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import (
    Category,
    Master,
    MasterSchema,
    Service,
    ServiceCreate,
    ServiceResponse,
)

app = FastAPI(
    title="Beauty Salon API",
    description="REST API для салона красоты: управление категориями, услугами и мастерами (FastAPI + SQLAlchemy + SQLite)",
    version="4.0.0",
)


@app.on_event("startup")
def on_startup():
    """При старте приложения создаем таблицы и загружаем тестовые данные."""
    init_db()


# ==========================================================
# 1. Эндпоинты услуг (Services - Задание: Pydantic ServiceCreate)
# ==========================================================

@app.post(
    "/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую услугу",
    description="Добавляет новую услугу в базу данных SQLite с валидацией через ServiceCreate (код 201).",
    responses={
        201: {
            "description": "Услуга успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "categoryId": 3,
                        "title": "Наращивание ресниц",
                        "desc": "Огромные ресницы уже через 30 минут",
                        "duration": 30,
                        "price": 1500.0,
                    }
                }
            },
        },
        422: {
            "description": "Ошибка валидации входных данных",
        },
    },
    tags=["Услуги"],
)
def create_service(service_in: ServiceCreate, db: Session = Depends(get_db)):
    """
    Задание 2: POST /services с использованием Pydantic-модели ServiceCreate.
    """
    db_service = Service(
        category_id=service_in.categoryId,
        title=service_in.title,
        desc=service_in.desc,
        duration=service_in.duration,
        price=service_in.price,
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@app.get(
    "/services",
    response_model=List[ServiceResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех услуг",
    tags=["Услуги"],
)
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@app.get(
    "/services/{service_id}",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить услугу по ID",
    tags=["Услуги"],
)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    return service


# ==========================================================
# 2. Эндпоинты мастеров (Masters - SQLAlchemy + SQLite)
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
        200: {"description": "Мастер успешно найден"},
        404: {"description": "Мастер не найден"},
    },
    tags=["Мастера"],
)
def get_master_by_id(master_id: int, db: Session = Depends(get_db)):
    master = db.query(Master).filter(Master.id == master_id).first()
    if master is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found",
        )
    return master


# ==========================================================
# 3. Эндпоинты категорий услуг (Categories)
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
    tags=["Категории"],
)
def get_categories():
    return CATEGORIES


@app.get(
    "/categories/{category_id}",
    response_model=Category,
    status_code=status.HTTP_200_OK,
    summary="Информация по категории",
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
            "POST /services",
            "GET /services",
            "GET /services/{service_id}",
            "GET /masters",
            "GET /masters?specialization={specialization}",
            "GET /masters/{master_id}",
            "GET /categories",
            "GET /categories/{category_id}",
        ],
    }
