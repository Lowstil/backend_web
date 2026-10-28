"""
Модульные тесты для проверки Pydantic-модели ServiceCreate и эндпоинта POST /services.
"""

import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from database import Base, get_db
from models import Service


class TestServicesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Изолированная тестовая SQLite БД в памяти
        cls.test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.test_engine
        )
        Base.metadata.create_all(bind=cls.test_engine)

        def override_get_db():
            db = cls.TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=cls.test_engine)

    def test_create_service_success_201(self):
        """Контрольный пример 1: Успешное создание услуги с кодом 201."""
        payload = {
            "categoryId": 3,
            "title": "Наращивание ресниц",
            "desc": "Огромные ресницы уже через 30 минут",
            "duration": 30,
            "price": 1500.00,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["categoryId"], 3)
        self.assertEqual(data["title"], "Наращивание ресниц")
        self.assertEqual(data["desc"], "Огромные ресницы уже через 30 минут")
        self.assertEqual(data["duration"], 30)
        self.assertEqual(data["price"], 1500.0)

    def test_create_service_invalid_price_type_422(self):
        """Контрольный пример 2: Ошибка валидации с кодом 422 при строковом значении price."""
        payload = {
            "categoryId": 3,
            "title": "Наращивание ресниц",
            "desc": "Огромные ресницы уже через 30 минут",
            "duration": 30,
            "price": "бесплатно",
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_service_invalid_fields_422(self):
        """Контрольный пример 3: Ошибка валидации с кодом 422 при пустом desc, duration=0, price=-1500."""
        payload = {
            "categoryId": 3,
            "title": "Наращивание ресниц",
            "desc": "",
            "duration": 0,
            "price": -1500.00,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_duration_boundary_min_valid(self):
        """Минимальная продолжительность 30 минут допустима."""
        payload = {
            "categoryId": 1,
            "title": "Экспресс-укладка",
            "desc": "Быстрая укладка волос",
            "duration": 30,
            "price": 1000.0,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_duration_boundary_max_valid(self):
        """Максимальная продолжительность 3 часа (180 минут) допустима."""
        payload = {
            "categoryId": 1,
            "title": "Сложное окрашивание",
            "desc": "Многоэтапное окрашивание и тонирование волос",
            "duration": 180,
            "price": 6000.0,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_duration_under_min_422(self):
        """Продолжительность менее 30 минут отклоняется (422)."""
        payload = {
            "categoryId": 1,
            "title": "Супер экспресс",
            "desc": "Слишком быстро",
            "duration": 29,
            "price": 500.0,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_duration_over_max_422(self):
        """Продолжительность более 3 часов (180 минут) отклоняется (422)."""
        payload = {
            "categoryId": 4,
            "title": "СПА весь день",
            "desc": "Очень долгая процедура",
            "duration": 181,
            "price": 10000.0,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_zero_price_422(self):
        """Стоимость равная 0 отклоняется (422)."""
        payload = {
            "categoryId": 2,
            "title": "Консультация",
            "desc": "Бесплатная консультация",
            "duration": 30,
            "price": 0.0,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_empty_title_422(self):
        """Пустое название отклоняется (422)."""
        payload = {
            "categoryId": 1,
            "title": "   ",
            "desc": "Нормальное описание",
            "duration": 45,
            "price": 800.0,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_title_too_long_422(self):
        """Название более 100 символов отклоняется (422)."""
        payload = {
            "categoryId": 1,
            "title": "А" * 101,
            "desc": "Нормальное описание",
            "duration": 45,
            "price": 800.0,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_desc_too_long_422(self):
        """Описание более 100 символов отклоняется (422)."""
        payload = {
            "categoryId": 1,
            "title": "Стрижка",
            "desc": "Б" * 101,
            "duration": 45,
            "price": 800.0,
        }
        response = self.client.post("/services", json=payload)
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
