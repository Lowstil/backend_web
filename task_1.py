"""
Задание 1. Класс Appoinment (запись клиента)

Перевести объект appointment из словаря в класс Appointment (Appoinment).
Функция create_appointment возвращает объект класса Appointment.
Объект записи создается только в том случае, если заполнены все поля.
"""

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


appointments: list[Appointment] = []


def create_appointment(
    client_name: str,
    master_id: int,
    service_id: int,
    time: str,
) -> Optional[Appointment]:
    """
    Создает объект записи клиента (класс Appointment).
    Запись создается только если заполнены все поля.
    """
    # Проверка, что переданы все необходимые поля и они не пустые
    if not client_name or not str(client_name).strip():
        return None
    if master_id is None or not isinstance(master_id, int):
        return None
    if service_id is None or not isinstance(service_id, int):
        return None
    if not time or not str(time).strip():
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
    print("=== Задание 1. Проверка работы ===")

    first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")

    print("Список записей:")
    for appointment in appointments:
        print(appointment.client_name, appointment.time)

    # Проверка с неполными данными
    test_empty_list: list[Appointment] = []
    appointments = test_empty_list
    no_correct_appointment = create_appointment("", 1, 1, "12:00")

    print("\nПроверка незаполненной записи:")
    print("appointments:", appointments)
    print("len(appointments):", len(appointments))
