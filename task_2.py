"""
Задание 2. Новое бизнес-правило

Записаться к мастеру можно только в часы работы салона: с 08:00 до 20:00.
"""

from datetime import time as dtime
from typing import Optional
from models import Appointment, Appoinment, Master, Service

# Справочники мастеров и услуг
MASTERS = {
    1: Master(1, "Иванов И.И."),
    2: Master(2, "Сергеев С.С."),
}

SERVICES = {
    1: Service(1, "Стрижка", 1500.0),
    2: Service(2, "Укладка", 2000.0),
}


def get_master(master_id: int) -> Optional[Master]:
    """Получить мастера по ID."""
    if not isinstance(master_id, int) or master_id <= 0:
        return None
    return MASTERS.get(master_id, Master(master_id, f"Мастер #{master_id}"))


def get_service(service_id: int) -> Optional[Service]:
    """Получить услугу по ID."""
    if not isinstance(service_id, int) or service_id <= 0:
        return None
    return SERVICES.get(service_id, Service(service_id, f"Услуга #{service_id}"))


def is_valid_working_time(time_str: str) -> bool:
    """
    Проверяет, входит ли время в часы работы салона: с 08:00 до 20:00.
    """
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
        # Салон работает с 08:00 до 20:00 включительно
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
    Запись создается только если:
    1. Заполнены все поля.
    2. Время находится в диапазоне с 08:00 до 20:00.
    """
    # 1. Проверка заполненности всех полей
    if not client_name or not str(client_name).strip():
        return None
    if master_id is None or not isinstance(master_id, int):
        return None
    if service_id is None or not isinstance(service_id, int):
        return None
    if not time or not str(time).strip():
        return None

    # 2. Проверка часов работы салона (с 08:00 до 20:00)
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


if __name__ == "__main__":
    print("=== Задание 2. Проверка работы ===")

    first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")

    print("Список записей:")
    for appointment in appointments:
        print(appointment.client_name, appointment.time)

    # Проверка с некорректным временем (00:00)
    test_empty_list: list[Appointment] = []
    appointments = test_empty_list
    no_correct_appointment = create_appointment("Сидорова А.А.", 1, 1, "00:00")

    print("\nПроверка некорректного времени ('00:00'):")
    print("appointments:", appointments)
    print("len(appointments):", len(appointments))
