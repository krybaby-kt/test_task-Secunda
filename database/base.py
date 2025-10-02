"""
Конфигурация базы данных SQLAlchemy.

Настраивает асинхронное подключение к PostgreSQL с пулом соединений,
создает сессионный объект и базовый класс для всех моделей.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from configuration.config import settings


# Асинхронный движок БД с настройками пула соединений
engine = create_async_engine(settings.DATABASE_URL_asyncpg, pool_size=25, max_overflow=50, pool_timeout=300)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()
