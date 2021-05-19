from ..core import settings
import pytest
import nest_asyncio
nest_asyncio.apply()

@pytest.mark.asyncio
async def test_create_service_and_get_service_by_salon_id(test_app):
    test_service = {
        "name": "Test Service",
        "estimatedTimeLower": 0,
        "estimatedTimeHigher": 100,
        "imageUrl": "https://1080motion.com/wp-content/uploads/2018/06/NoImageFound.jpg.png",
        "price": "999.99",
        "rating": "5.0",
        "description": "Test Description",
        "salon_id": "none"
    }

    first_response = test_app.post("/services/new", json=test_service)
    assert first_response.status_code == 201
    assert first_response.json().get('message') == "Service added successfully"
    deleted_service = await test_app.mongodb[settings.MONGODB_COLLECTION_SERVICES].find_one_and_delete({"_id": first_response.json().get("data")["_id"]})
    assert deleted_service is not None

    test_request = {
        "id" : "60861a4e1289ea8e013c7a41"
    }

    second_response = test_app.post("/services/get", json=test_request)
    assert second_response.status_code == 200
    assert second_response.json().get("message") == "List retrieved successfully"
    assert second_response.json().get("data")[0]["_id"] == "60861aa01289ea8e013c7a43"
