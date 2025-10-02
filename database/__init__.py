from database.base import engine, Base


async def init_models():
    """
    Инициализирует модели в базе данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
