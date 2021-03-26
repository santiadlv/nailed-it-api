import pytest
import mongomock
from ..main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def test_app():
    app.mongodb_client = mongomock.MongoClient()
    app.mongodb = app.mongodb_client.db
    client = TestClient(app)
    yield client