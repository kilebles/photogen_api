import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise
from unittest.mock import patch

from photogen_api.main import app
from photogen_api.config import config


async def truncate_tables():
    for model in Tortoise.apps["models"].values():
        await model.all().delete()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def initialize_tests():
    await Tortoise.init(
        db_url=config.DATABASE_URL,
        modules={"models": ["photogen_api.database.models"]},
    )
    await Tortoise.generate_schemas()
    await truncate_tables()
    yield
    await Tortoise.close_connections()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def mock_signature_check():
    with patch("photogen_api.services.auth_service.web_app.check_webapp_signature", return_value=True):
        yield
