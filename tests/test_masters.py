"""
Модульные тесты для проверки SQLAlchemy модели Master и API эндпоинтов /masters.
"""

import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from database import Base, get_db
from models import Master


class TestMastersAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем изолированную базу в памяти с StaticPool для тестов
        cls.test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.test_engine
        )
        Base.metadata.create_all(bind=cls.test_engine)

        # Заполняем тестовыми данными
        with cls.TestingSessionLocal() as session:
            session.add_all([
                Master(id=1, name="Анна", specialization="Парикмахер"),
                Master(id=2, name="Мария", specialization="Визажист"),
            ])
            session.commit()

        # Переопределяем зависимость get_db для тестового клиента
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

    def test_model_fields(self):
        """Проверка полей модели Master."""
        master = Master(id=10, name="Ольга", specialization="Косметолог")
        self.assertEqual(master.id, 10)
        self.assertEqual(master.name, "Ольга")
        self.assertEqual(master.specialization, "Косметолог")
        self.assertEqual(master.master_id, 10)
        self.assertEqual(Master.__tablename__, "masters")

    def test_get_all_masters(self):
        """GET /masters возвращает всех мастеров из БД со статусом 200."""
        response = self.client.get("/masters")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {"id": 1, "name": "Анна", "specialization": "Парикмахер"})
        self.assertEqual(data[1], {"id": 2, "name": "Мария", "specialization": "Визажист"})

    def test_get_masters_by_specialization(self):
        """GET /masters?specialization=Парикмахер фильтрует мастеров по специализации."""
        response = self.client.get("/masters", params={"specialization": "Парикмахер"})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Анна")
        self.assertEqual(data[0]["specialization"], "Парикмахер")

    def test_get_masters_by_nonexistent_specialization(self):
        """GET /masters?specialization=Неизвестно возвращает пустой список."""
        response = self.client.get("/masters", params={"specialization": "Массажист"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_master_by_id_success(self):
        """GET /masters/{master_id} возвращает мастера по ID со статусом 200."""
        response = self.client.get("/masters/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "name": "Анна", "specialization": "Парикмахер"},
        )

        response_2 = self.client.get("/masters/2")
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(
            response_2.json(),
            {"id": 2, "name": "Мария", "specialization": "Визажист"},
        )

    def test_get_master_by_id_not_found(self):
        """GET /masters/{master_id} возвращает 404, если мастер не найден."""
        response = self.client.get("/masters/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Master not found"})

    def test_get_master_by_invalid_id_type(self):
        """GET /masters/{master_id} возвращает 422 при некорректном типе ID."""
        response = self.client.get("/masters/not-a-number")
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
