import pytest
from ..main import app
from ..core import settings
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture(scope="module")
def test_app():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_NAME]
    client = TestClient(app)
    client.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    client.mongodb = app.mongodb_client[settings.MONGODB_NAME]
    yield client