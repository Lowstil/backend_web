"""
Задание 1. Модель Master

Создайте SQLAlchemy-модель Master и таблицу masters.
Мастер содержит минимум три поля:
- id
- name
- specialization
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from models import Master

# Создаем тестовую локальную SQLite базу
DATABASE_URL = "sqlite:///./salon.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_masters_table():
    # Создаем таблицы в SQLite
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # Проверяем наличие записей
        if db.query(Master).count() == 0:
            masters_data = [
                Master(id=1, name="Анна", specialization="Парикмахер"),
                Master(id=2, name="Мария", specialization="Визажист"),
            ]
            db.add_all(masters_data)
            db.commit()


if __name__ == "__main__":
    print("=== Проверка Задания 1: Создание модели Master и таблицы masters ===")
    init_masters_table()

    with SessionLocal() as db:
        masters = db.query(Master).all()
        print(f"\nЗаписей в таблице '{Master.__tablename__}': {len(masters)}")
        print(f"{'id':<5} {'name':<15} {'specialization':<20}")
        print("-" * 40)
        for m in masters:
            print(f"{m.id:<5} {m.name:<15} {m.specialization:<20}")
