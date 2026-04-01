from sqlalchemy.ext.asyncio import async_sessionmaker

from app.infrastructure.database.adapters.pg_connection import engine

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session
