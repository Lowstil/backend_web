"""
Модульные тесты для проверки эндпоинтов категорий (Задания 1 и 2).
"""

import unittest
from fastapi.testclient import TestClient
from app import app, CATEGORIES


class TestCategoryEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_all_categories_status_200(self):
        """GET /categories возвращает код 200 и полный список категорий."""
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)

        # Проверяем структуру элементов списка
        expected_names = [
            "Стрижки и укладки",
            "Маникюр и педикюр",
            "Брови и ресницы",
            "Спа-процедуры",
        ]
        for idx, item in enumerate(data):
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("servicesCount", item)
            self.assertEqual(item["id"], idx + 1)
            self.assertEqual(item["name"], expected_names[idx])
            self.assertIsInstance(item["servicesCount"], int)

    def test_get_category_by_id_success(self):
        """GET /categories/{category_id} возвращает 200 и данные категории при корректном ID."""
        for expected in CATEGORIES:
            cat_id = expected["id"]
            response = self.client.get(f"/categories/{cat_id}")
            self.assertEqual(response.status_code, 200)

            data = response.json()
            self.assertEqual(data["id"], expected["id"])
            self.assertEqual(data["name"], expected["name"])
            self.assertEqual(data["servicesCount"], expected["servicesCount"])

    def test_get_category_by_id_first_category(self):
        """Проверка контрольного примера из задания для id=1."""
        response = self.client.get("/categories/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
        )

    def test_get_category_by_id_not_found(self):
        """GET /categories/{category_id} возвращает 404, если категории не существует."""
        response = self.client.get("/categories/999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("detail", data)
        self.assertEqual(data["detail"], "Category not found")

    def test_get_category_by_id_invalid_type(self):
        """GET /categories/{category_id} возвращает 422 при нечисловом ID."""
        response = self.client.get("/categories/not-a-number")
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
