"""
Модульные тесты для проверки корректности работы create_appointment и класса Appointment.
"""

import unittest
from main import (
    Appointment,
    Appoinment,
    create_appointment,
    appointments,
    is_valid_working_time,
)


class TestAppointment(unittest.TestCase):
    def setUp(self):
        # Очищаем список записей перед каждым тестом
        appointments.clear()

    def test_class_appointment_creation(self):
        """Проверка создания объекта класса Appointment."""
        app = Appointment(1, "Тестов Т.Т.", 1, 1, "10:00")
        self.assertIsInstance(app, Appointment)
        self.assertEqual(app.id, 1)
        self.assertEqual(app.client_name, "Тестов Т.Т.")
        self.assertEqual(app.master_id, 1)
        self.assertEqual(app.service_id, 1)
        self.assertEqual(app.time, "10:00")

    def test_appoinment_alias(self):
        """Проверка алиаса Appoinment."""
        self.assertIs(Appointment, Appoinment)

    def test_valid_appointments(self):
        """Проверка успешного создания записей."""
        first = create_appointment("Иванова А.А.", 1, 1, "10:00")
        second = create_appointment("Петрова А.А.", 1, 1, "11:00")

        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertEqual(len(appointments), 2)
        self.assertEqual(appointments[0].client_name, "Иванова А.А.")
        self.assertEqual(appointments[1].client_name, "Петрова А.А.")

    def test_missing_fields(self):
        """Проверка отклонения записей с пустыми полями."""
        # Пустое имя
        res1 = create_appointment("", 1, 1, "12:00")
        self.assertIsNone(res1)
        # Пустое время
        res2 = create_appointment("Иванова А.А.", 1, 1, "")
        self.assertIsNone(res2)
        # Несуществующий мастер (<= 0)
        res3 = create_appointment("Иванова А.А.", 0, 1, "12:00")
        self.assertIsNone(res3)
        # Список должен остаться пустым
        self.assertEqual(len(appointments), 0)

    def test_working_hours_validation(self):
        """Проверка правила часов работы салона (с 08:00 до 20:00)."""
        # Корректное время
        self.assertTrue(is_valid_working_time("08:00"))
        self.assertTrue(is_valid_working_time("10:00"))
        self.assertTrue(is_valid_working_time("20:00"))

        # Некорректное время
        self.assertFalse(is_valid_working_time("00:00"))
        self.assertFalse(is_valid_working_time("07:59"))
        self.assertFalse(is_valid_working_time("20:01"))
        self.assertFalse(is_valid_working_time("23:59"))
        self.assertFalse(is_valid_working_time("invalid_time"))

    def test_appointment_outside_working_hours_rejected(self):
        """Запись вне рабочих часов не должна создаваться."""
        res = create_appointment("Сидорова А.А.", 1, 1, "00:00")
        self.assertIsNone(res)
        self.assertEqual(len(appointments), 0)


if __name__ == "__main__":
    unittest.main()
