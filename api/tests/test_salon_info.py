from ..core import settings
import asyncio
import pytest
import pytest_asyncio.plugin
import nest_asyncio
nest_asyncio.apply()
from fastapi import status

@pytest.mark.asyncio
async def test_get_salon_info_by_id(test_app):
    id = "6085d9afd9827ab0f5273e3b"
    response = test_app.get(f"/salons/{id}")
    data = (response.json().get('data'))
    assert response.status_code == status.HTTP_200_OK

    info = await test_app.mongodb[settings.MONGODB_COLLECTION_SALONS].find_one({"_id": id})
    assert data == info