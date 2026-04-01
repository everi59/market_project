from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import QueuePool
from app.infrastructure.config.config import DB_CONFIG, APP_CONFIG
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(self):
        logger.info(f"Creating database engine for {DB_CONFIG.DB_HOST}:{DB_CONFIG.DB_PORT}")

        self._engine = create_async_engine(
            url=DB_CONFIG.get_url(is_async=True),
            poolclass=QueuePool,
            pool_size=DB_CONFIG.DB_POOL_SIZE,
            max_overflow=DB_CONFIG.DB_MAX_OVERFLOW,
            pool_timeout=DB_CONFIG.DB_POOL_TIMEOUT,
            pool_recycle=DB_CONFIG.DB_POOL_RECYCLE,
            echo=APP_CONFIG.DEBUG,
        )

        self._session_maker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

        logger.info("Database engine created successfully")

    def get_session(self) -> AsyncSession:
        return self._session_maker()

    async def health_check(self) -> bool:
        from sqlalchemy import text
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    async def close(self):
        logger.info("Closing database connections")
        await self._engine.dispose()
        logger.info("Database connections closed")