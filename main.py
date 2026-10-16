"""
Лабораторная работа: Решение заданий 1 и 2
Тема: ООП в Python, валидация данных и бизнес-логика записи клиентов.
"""

from datetime import time as dtime
from typing import Optional


# ==========================================================
# 1. Модели данных (Models)
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
    """Класс записи клиента на услугу (Задание 1)."""

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
# 2. Имитация базы данных и вспомогательные функции
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
    """
    Проверка часов работы салона: с 08:00 до 20:00 (Задание 2).
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
        return dtime(8, 0) <= appointment_time <= dtime(20, 0)
    except (ValueError, TypeError, AttributeError):
        return False


# ==========================================================
# 3. Основная функция создания записи
# ==========================================================

appointments: list[Appointment] = []


def create_appointment(
    client_name: str,
    master_id: int,
    service_id: int,
    time: str,
) -> Optional[Appointment]:
    """
    Создает объект записи клиента (класс Appointment).
    
    Условия создания записи:
    1. Заполнены все поля (клиент, мастер, услуга, время).
    2. Время находится в интервале рабочих часов салона: с 08:00 до 20:00.
    """
    # Проверка заполненности всех полей
    if not client_name or not str(client_name).strip():
        return None
    if master_id is None or not isinstance(master_id, int):
        return None
    if service_id is None or not isinstance(service_id, int):
        return None
    if not time or not str(time).strip():
        return None

    # Проверка бизнес-правила часов работы (с 08:00 до 20:00)
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
# 4. Проверочные сценарии из условий заданий
# ==========================================================

def run_tests():
    global appointments

    print("--------------------------------------------------")
    print("Задание 1 и 2: Создание корректных записей")
    print("--------------------------------------------------")
    appointments = []

    first_appointment = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second_appointment = create_appointment("Петрова А.А.", 1, 1, "11:00")

    print("Список записей:")
    for appointment in appointments:
        print(appointment.client_name, appointment.time)

    print("\n--------------------------------------------------")
    print("Задание 1: Создать запись, где частично не заполнены поля")
    print("--------------------------------------------------")
    appointments = []
    no_correct_appointment = create_appointment("", 1, 1, "12:00")

    print("Результат проверки appointments:")
    print(appointments)
    print("Длина appointments (len):", len(appointments))

    print("\n--------------------------------------------------")
    print("Задание 2: Создать запись с некорректным временем (00:00)")
    print("--------------------------------------------------")
    appointments = []
    no_correct_appointment_time = create_appointment("Сидорова А.А.", 1, 1, "00:00")

    print("Результат проверки appointments:")
    print(appointments)
    print("Длина appointments (len):", len(appointments))


if __name__ == "__main__":
    run_tests()
