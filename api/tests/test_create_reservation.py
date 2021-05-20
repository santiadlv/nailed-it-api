from ..core import settings
import pytest 
import nest_asyncio
from fastapi import status
nest_asyncio.apply()

@pytest.mark.asyncio
async def test_get_reservation_success(test_app):
    test_add_hour_available = {
        "service_id": "60860830041aa13d76554242", 
        "timeStart": 870,
        "timeEnd": 900
    }

    new_hour = test_app.post("/hours/update/add", json=test_add_hour_available)
    new_hour_id = new_hour.json().get("data")["hours"][-1]["hour_id"]
    assert new_hour.json().get("message") == "Successfully added an hour to the service's availability"

    test_reservation = {
        "user_id": "605cd9ca1ec4bf19fe3f9581",        
        "service_id": test_add_hour_available["service_id"], 
        "hour_id": new_hour_id,
        "time_start": test_add_hour_available["timeStart"],
        "time_end": test_add_hour_available["timeEnd"]
    }

    new_reservation = test_app.post("/reservations/new", json=test_reservation)
    assert new_reservation.status_code == 201
    assert new_reservation.json().get("message") == "Reservation added successfully"

    available_hour = await test_app.mongodb[settings.MONGODB_COLLECTION_HOURS].find_one({"service_id": "60860830041aa13d76554242", "hours": [{"hour_id": new_hour_id}]})
    assert available_hour is None


    # GET ALL THE RESERVATIONS FROM THE PREVIOUS USER
    user_id = new_reservation.json().get("data")["user_id"]
    all_reservations = test_app.get(f"/reservations/list/{user_id}")

    # GET THE ID FOR THE LAST RESERVATION CREATED
    reservation_id = all_reservations.json().get("data")[-1]["_id"]
    # DELETE THE RESERVATION CREATED 
    delete_reservation = await test_app.mongodb[settings.MONGODB_COLLECTION_RESERVATIONS].find_one_and_delete({"_id": reservation_id})
    assert delete_reservation is not None

    
