from ..core import settings
from fastapi import status
import pytest, nest_asyncio
nest_asyncio.apply()

@pytest.mark.asyncio
async def test_insert_hours_for_mock_service(test_app):
    new_hours = {
        "service_id": "TEST-SERVICE",
        "hours": [
            {
                "timeStart": 0,
                "timeEnd": 1439
            }
        ]
    }

    response1 = test_app.post("/hours/insert", json=new_hours)
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.json().get("message") == "Availability hours inserted successfully"

    response2 = test_app.post("/hours/insert", json=new_hours)
    assert response2.status_code == status.HTTP_409_CONFLICT
    assert response2.json().get("detail") == "Availability hours for service with ID TEST-SERVICE already exist"

    deleted_hours = await test_app.mongodb[settings.MONGODB_COLLECTION_HOURS].find_one_and_delete({"_id": response1.json().get("data")["_id"]})
    assert deleted_hours is not None
