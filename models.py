from typing import Optional
from pydantic import BaseModel, Field


# ==========================================================
# Модели из Задания 1 и 2 (Запись клиентов)
# ==========================================================

class Master:
    """Модель мастера салона."""

    def __init__(self, master_id: int, name: str = ""):
        self.master_id = master_id
        self.name = name

    def __repr__(self) -> str:
        return f"Master(id={self.master_id}, name='{self.name}')"


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


# ==========================================================
# Модели для Эндпоинтов (Категории услуг)
# ==========================================================

class Category(BaseModel):
    """Pydantic-модель категории услуг салона."""

    id: int = Field(..., description="Уникальный идентификатор категории")
    name: str = Field(..., description="Название категории услуг")
    servicesCount: int = Field(..., description="Количество услуг в категории")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Стрижки и укладки",
                "servicesCount": 5,
            }
        }
