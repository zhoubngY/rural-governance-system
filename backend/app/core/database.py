from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from app.core.config import settings
from contextvars import ContextVar
from typing import Optional

tenant_schema_var: ContextVar[Optional[str]] = ContextVar("tenant_schema", default=None)

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=False
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        tenant_schema = tenant_schema_var.get()
        if tenant_schema:
            await session.execute(text(f'SET search_path TO "{tenant_schema}", public'))
        try:
            yield session
        finally:
            await session.close()
