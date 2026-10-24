"""
Настройка подключения к SQLite базе данных через SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./salon.db"

# Движок для SQLite базы данных (connect_args={'check_same_thread': False} для FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Фабрика сессий БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый декларативный класс для моделей
Base = declarative_base()


def get_db():
    """Генератор сессии базы данных для FastAPI Dependency Injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Инициализация базы данных и наполнение таблицы masters тестовыми данными."""
    from models import Master

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # Проверяем, есть ли уже записи в таблице masters
        if db.query(Master).count() == 0:
            initial_masters = [
                Master(id=1, name="Анна", specialization="Парикмахер"),
                Master(id=2, name="Мария", specialization="Визажист"),
            ]
            db.add_all(initial_masters)
            db.commit()
