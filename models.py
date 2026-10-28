from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import Column, Float, Integer, String

from database import Base


# ==========================================================
# 1. SQLAlchemy Модели (Таблицы в SQLite БД)
# ==========================================================

class Master(Base):
    """
    SQLAlchemy-модель мастера салона.
    Таблица: masters
    Поля: id, name, specialization
    """

    __tablename__ = "masters"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    @property
    def master_id(self) -> int:
        """Для обратной совместимости с логикой записей (appointment)."""
        return self.id

    def __repr__(self) -> str:
        return f"<Master(id={self.id}, name='{self.name}', specialization='{self.specialization}')>"


class Service(Base):
    """
    SQLAlchemy-модель услуги салона.
    Таблица: services
    Поля: id, category_id, title, desc, duration, price
    """

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    category_id = Column(Integer, nullable=False, index=True)
    title = Column(String(100), nullable=False)
    desc = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    @property
    def categoryId(self) -> int:
        return self.category_id

    @property
    def service_id(self) -> int:
        return self.id

    @property
    def name(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return (
            f"<Service(id={self.id}, category_id={self.category_id}, "
            f"title='{self.title}', duration={self.duration}, price={self.price})>"
        )


# ==========================================================
# 2. Pydantic-схемы для валидации и сериализации в API
# ==========================================================

class ServiceCreate(BaseModel):
    """
    Pydantic-модель для создания новой услуги (Задание 1).
    Поля:
    - categoryId: идентификатор категории
    - title: название услуги (не пустое, макс 100 символов)
    - desc: описание услуги (не пустое, макс 100 символов)
    - duration: продолжительность (от 30 мин до 180 мин / 3 часов)
    - price: стоимость (больше 0)
    """

    categoryId: int = Field(..., description="Идентификатор категории")
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Название услуги (не может быть пустым, макс 100 символов)",
    )
    desc: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Описание услуги (не может быть пустым, макс 100 символов)",
    )
    duration: int = Field(
        ...,
        ge=30,
        le=180,
        description="Продолжительность услуги в минутах (от 30 до 180 минут)",
    )
    price: float = Field(
        ...,
        gt=0,
        description="Стоимость услуги (должна быть строго больше 0)",
    )

    @field_validator("title", "desc")
    @classmethod
    def check_not_empty_whitespace(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Поле не может быть пустым или состоять только из пробелов")
        return v.strip()

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "categoryId": 3,
                "title": "Наращивание ресниц",
                "desc": "Огромные ресницы уже через 30 минут",
                "duration": 30,
                "price": 1500.00,
            }
        },
    )


class ServiceResponse(BaseModel):
    """Pydantic-схема ответа с данными об услуге."""

    id: int
    categoryId: int
    title: str
    desc: str
    duration: int
    price: float

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class MasterSchema(BaseModel):
    """Pydantic-схема для отображения мастера в API."""

    id: int = Field(..., description="Идентификатор мастера")
    name: str = Field(..., description="Имя мастера")
    specialization: str = Field(..., description="Специализация мастера")

    model_config = ConfigDict(from_attributes=True)


class Category(BaseModel):
    """Pydantic-модель категории услуг салона."""

    id: int = Field(..., description="Уникальный идентификатор категории")
    name: str = Field(..., description="Название категории услуг")
    servicesCount: int = Field(..., description="Количество услуг в категории")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Стрижки и укладки",
                "servicesCount": 5,
            }
        },
    )


# ==========================================================
# 3. Модели для логики записей клиентов (Appointment)
# ==========================================================

class Appointment:
    """Класс записи клиента на услугу."""

    def __init__(
        self,
        id: int,
        client_name: str,
        master_id: int,
        service_id: int,
        time: str,
    ):
        self.id = id
        self.client_name = client_name
        self.master_id = master_id
        self.service_id = service_id
        self.time = time

    def __repr__(self) -> str:
        return (
            f"Appointment(id={self.id}, client_name='{self.client_name}', "
            f"master_id={self.master_id}, service_id={self.service_id}, time='{self.time}')"
        )


# Поддержка названия из формулировки задания (Appoinment без буквы 't')
Appoinment = Appointment
