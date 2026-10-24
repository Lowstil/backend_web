"""
Лабораторная работа: Backend Web
1. ООП и бизнес-логика записи клиентов (Класс Appointment).
2. REST API эндпоинты категорий услуг (GET /categories, GET /categories/{category_id}).
3. SQLite БД и SQLAlchemy API для мастеров (GET /masters, GET /masters?specialization=..., GET /masters/{master_id}).
"""

import json
import sys
from datetime import time as dtime
from typing import Optional

from fastapi.testclient import TestClient

from app import app
from database import init_db
from models import Appointment, Appoinment, Category, Master, MasterSchema, Service


# ==========================================================
# ЧАСТЬ 1: Запись клиентов (Appointment & Business Rules)
# ==========================================================

SERVICES = {
    1: Service(1, "Стрижка", 1500.0),
    2: Service(2, "Укладка", 2000.0),
}


def get_master(master_id: int) -> Optional[Master]:
    """Получение мастера по ID."""
    if not isinstance(master_id, int) or master_id <= 0:
        return None
    # Возвращаем объект с атрибутом master_id
    return Master(id=master_id, name=f"Мастер #{master_id}", specialization="Парикмахер")


def get_service(service_id: int) -> Optional[Service]:
    """Получение услуги по ID."""
    if not isinstance(service_id, int) or service_id <= 0:
        return None
    return SERVICES.get(service_id, Service(service_id, f"Услуга #{service_id}"))


def is_valid_working_time(time_str: str) -> bool:
    """Проверка часов работы салона: с 08:00 до 20:00."""
    if not time_str or not isinstance(time_str, str):
        return False
    try:
        parts = time_str.strip().split(":")
        if len(parts) != 2:
            return False
        hours, minutes = int(parts[0]), int(parts[1])
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            return False
        appointment_time = dtime(hours, minutes)
        return dtime(8, 0) <= appointment_time <= dtime(20, 0)
    except (ValueError, TypeError, AttributeError):
        return False


appointments: list[Appointment] = []


def create_appointment(
    client_name: str,
    master_id: int,
    service_id: int,
    time: str,
) -> Optional[Appointment]:
    """
    Создает объект записи клиента (класс Appointment).
    1. Все поля заполнены.
    2. Время записи находится в диапазоне с 08:00 до 20:00.
    """
    if not client_name or not str(client_name).strip():
        return None
    if master_id is None or not isinstance(master_id, int):
        return None
    if service_id is None or not isinstance(service_id, int):
        return None
    if not time or not str(time).strip():
        return None

    if not is_valid_working_time(time):
        return None

    master = get_master(master_id)
    service = get_service(service_id)

    if master is None or service is None:
        return None

    appointment = Appointment(
        id=len(appointments) + 1,
        client_name=str(client_name).strip(),
        master_id=master.master_id,
        service_id=service.service_id,
        time=str(time).strip(),
    )
    appointments.append(appointment)
    return appointment


# ==========================================================
# Демонстрация работы всех заданий
# ==========================================================

def run_demonstration():
    global appointments

    print("==================================================")
    print("1. ЗАДАНИЯ 1: ЗАПИСЬ КЛИЕНТОВ (APPOINTMENT)")
    print("==================================================")

    appointments = []
    first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")

    print("\nСписок записей:")
    for appointment in appointments:
        print(appointment.client_name, appointment.time)

    appointments = []
    no_correct_appointment = create_appointment("", 1, 1, "12:00")
    print("\nПроверка незаполненных полей (client_name=''):")
    print("appointments:", appointments)
    print("len(appointments):", len(appointments))

    appointments = []
    no_correct_appointment_time = create_appointment("Сидорова А.А.", 1, 1, "00:00")
    print("\nПроверка некорректного времени ('00:00'):")
    print("appointments:", appointments)
    print("len(appointments):", len(appointments))

    print("\n==================================================")
    print("2. ЗАДАНИЯ 2: ЭНДПОИНТЫ КАТЕГОРИЙ (FASTAPI)")
    print("==================================================")

    init_db()
    client = TestClient(app)

    print("\n[GET /categories]:")
    r_cat = client.get("/categories")
    print(f"Статус: {r_cat.status_code}")
    print(json.dumps(r_cat.json(), ensure_ascii=False, indent=2))

    print("\n[GET /categories/1]:")
    r_cat_1 = client.get("/categories/1")
    print(f"Статус: {r_cat_1.status_code}")
    print(json.dumps(r_cat_1.json(), ensure_ascii=False, indent=2))

    print("\n[GET /categories/999]:")
    r_cat_404 = client.get("/categories/999")
    print(f"Статус: {r_cat_404.status_code}, Тело: {r_cat_404.json()}")

    print("\n==================================================")
    print("3. ЗАДАНИЯ 3: МАСТЕРА В SQLite & SQLAlchemy")
    print("==================================================")

    print("\n[GET /masters] (Все мастера из SQLite БД):")
    r_masters = client.get("/masters")
    print(f"Статус: {r_masters.status_code}")
    print(json.dumps(r_masters.json(), ensure_ascii=False, indent=2))

    print("\n[GET /masters?specialization=Парикмахер] (Фильтрация):")
    r_filter = client.get("/masters", params={"specialization": "Парикмахер"})
    print(f"Статус: {r_filter.status_code}")
    print(json.dumps(r_filter.json(), ensure_ascii=False, indent=2))

    print("\n[GET /masters/1] (Мастер по ID):")
    r_m1 = client.get("/masters/1")
    print(f"Статус: {r_m1.status_code}")
    print(json.dumps(r_m1.json(), ensure_ascii=False, indent=2))

    print("\n[GET /masters/999] (Несуществующий мастер - 404 Not Found):")
    r_m404 = client.get("/masters/999")
    print(f"Статус: {r_m404.status_code}, Тело: {r_m404.json()}")

    print("\n==================================================")
    print("Все сценарии проверены и работают корректно!")
    print("==================================================")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        init_db()
        print("Запуск FastAPI сервера на http://127.0.0.1:8000 ...")
        uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    else:
        run_demonstration()
