import asyncio
from typing import AsyncGenerator

import pytest


from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from config.settings import POSTGRES_USER_TEST, POSTGRES_PASSWORD_TEST, POSTGRES_HOST_TEST, POSTGRES_PORT_TEST, POSTGRES_DB_TEST
from database.db_config import get_async_session, metadata
from main import app

test_engine = create_async_engine(
    f"postgresql+asyncpg://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}@{POSTGRES_HOST_TEST}:{POSTGRES_PORT_TEST}/{POSTGRES_DB_TEST}",
    echo=True,
)

async_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


client = TestClient(app)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_async():
    assert True
