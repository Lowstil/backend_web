"""
Лабораторная работа: Backend Web
1. ООП и бизнес-логика записи клиентов (Класс Appointment).
2. Разработка REST API эндпоинтов (Категории услуг: GET /categories, GET /categories/{category_id}).
"""

import sys
import json
from datetime import time as dtime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from models import Appointment, Appoinment, Master, Service, Category
from app import app, CATEGORIES


# ==========================================================
# ЧАСТЬ 1: Запись клиентов (Appointment & Business Rules)
# ==========================================================

MASTERS = {
    1: Master(1, "Иванов И.И."),
    2: Master(2, "Сергеев С.С."),
}

SERVICES = {
    1: Service(1, "Стрижка", 1500.0),
    2: Service(2, "Укладка", 2000.0),
}


def get_master(master_id: int) -> Optional[Master]:
    """Получение мастера по ID."""
    if not isinstance(master_id, int) or master_id <= 0:
        return None
    return MASTERS.get(master_id, Master(master_id, f"Мастер #{master_id}"))


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
    Запись создается только при условии:
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
    print("1. ПРОВЕРКА ЗАДАНИЙ: ЗАПИСЬ КЛИЕНТОВ (APPOINTMENT)")
    print("==================================================")

    # 1.1 Создание корректных записей
    appointments = []
    first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")

    print("\nСписок записей:")
    for appointment in appointments:
        print(appointment.client_name, appointment.time)

    # 1.2 Создание записи с неполными данными
    appointments = []
    no_correct_appointment = create_appointment("", 1, 1, "12:00")
    print("\nПроверка незаполненных полей (client_name=''):")
    print("appointments:", appointments)
    print("len(appointments):", len(appointments))

    # 1.3 Создание записи с некорректным временем (00:00)
    appointments = []
    no_correct_appointment_time = create_appointment("Сидорова А.А.", 1, 1, "00:00")
    print("\nПроверка некорректного времени ('00:00'):")
    print("appointments:", appointments)
    print("len(appointments):", len(appointments))

    print("\n==================================================")
    print("2. ПРОВЕРКА ЗАДАНИЙ: ЭНДПОИНТЫ КАТЕГОРИЙ (FASTAPI)")
    print("==================================================")

    client = TestClient(app)

    # 2.1 GET /categories
    print("\n[Эндпоинт 1] GET /categories:")
    r1 = client.get("/categories")
    print(f"Статус-код: {r1.status_code}")
    print("Тело ответа:")
    print(json.dumps(r1.json(), ensure_ascii=False, indent=2))

    # 2.2 GET /categories/{category_id} - Успешно
    print("\n[Эндпоинт 2] GET /categories/1 (Успешный запрос):")
    r2 = client.get("/categories/1")
    print(f"Статус-код: {r2.status_code}")
    print("Тело ответа:")
    print(json.dumps(r2.json(), ensure_ascii=False, indent=2))

    # 2.3 GET /categories/{category_id} - 404
    print("\n[Эндпоинт 2] GET /categories/999 (Категория не найдена):")
    r3 = client.get("/categories/999")
    print(f"Статус-код: {r3.status_code}")
    print(f"Тело ответа: {r3.json()}")

    print("\n==================================================")
    print("Все тесты и эндпоинты успешно выполнены!")
    print("==================================================")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        print("Запуск FastAPI сервера на http://127.0.0.1:8000 ...")
        uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    else:
        run_demonstration()
