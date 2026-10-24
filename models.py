from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Column, Integer, String

from database import Base


# ==========================================================
# 1. SQLAlchemy Модели (Таблицы БД)
# ==========================================================

class Master(Base):
    """
    SQLAlchemy-модель мастера салона (Задание 1).
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


# ==========================================================
# 2. Pydantic-схемы (Для валидации и сериализации в API)
# ==========================================================

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
# 3. Модели услуг и записей (Appointment / Service)
# ==========================================================

class Service:
    """Модель услуги салона."""

    def __init__(self, service_id: int, name: str = "", price: float = 0.0):
        self.service_id = service_id
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return f"Service(id={self.service_id}, name='{self.name}', price={self.price})"


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
