from ..core import settings
import pytest 
import nest_asyncio
from fastapi import status
from pytest import fail
nest_asyncio.apply()

@pytest.mark.asyncio
async def test_get_reservation_success(test_app):

    # CREATE A NEW HOUR IN A GIVEN SERVICE
    test_add_hour_available = {
        "service_id": "60860830041aa13d76554242", 
        "timeStart": 870,
        "timeEnd": 900
    }

    # ADD NEW HOUR
    new_hour = test_app.post("/hours/update/add", json=test_add_hour_available)
    new_hour_id = new_hour.json().get("data")["hours"][-1]["hour_id"]
    assert new_hour.json().get("message") == "Successfully added an hour to the service's availability"

    # CREATE A NEW RESERVATION WITH THE PREVIOUS NEW ADDED HOURS 
    test_reservation = {
        "user_id": "605cd9ca1ec4bf19fe3f9581",        
        "service_id": test_add_hour_available["service_id"], 
        "hour_id": new_hour_id,
        "time_start": test_add_hour_available["timeStart"],
        "time_end": test_add_hour_available["timeEnd"]
    }

    # TEST IT WAS SUCCESFUL 
    new_reservation = test_app.post("/reservations/new", json=test_reservation)
    assert new_reservation.status_code == 201
    assert new_reservation.json().get("message") == "Reservation added successfully"

    # TEST THE HOUR IN THE GIVEN SERVICE IS NO LONGER AVAILABLE
    available_hour = await test_app.mongodb[settings.MONGODB_COLLECTION_HOURS].find_one({"service_id": "60860830041aa13d76554242", "hours": [{"hour_id": new_hour_id}]})
    assert available_hour is None

    # GET ALL THE RESERVATIONS FROM THE PREVIOUS USER
    user_id = new_reservation.json().get("data")["user_id"]
    all_reservations = test_app.get(f"/reservations/list/{user_id}")

    # GET THE ID FOR THE LAST RESERVATION CREATED
    reservation_id = all_reservations.json().get("data")[-1]["_id"]

    # GET THAT RESERVATION AND ASSERT IS NOT NONE
    reservation = test_app.get(f"/reservations/{user_id}/{reservation_id}")
    assert reservation is not None

    # RESERVATION TO CANCEL
    test_reservation_to_cancel = {
        "service_id": reservation.json().get("data")["service_id"], 
        "timeStart": reservation.json().get("data")["time_start"],
        "timeEnd": reservation.json().get("data")["time_end"]
    }

    # CANCEL THE RESERVATION 
    cancel_reservation = test_app.post(f"/reservations/cancel/{reservation_id}", json=test_reservation_to_cancel)
    assert cancel_reservation.json().get("message") == "Successfully added the availabile hour"

    reservation_cancelled = test_app.get(f"/reservations/{user_id}/{reservation_id}")
    assert reservation_cancelled.status_code == 404
    assert reservation_cancelled.json().get("detail") == f"User with ID {user_id} and reservation with ID {reservation_id} was not found"

    test_service_hours = {  
        "service_id": test_reservation_to_cancel["service_id"]
    }

    # TEST THE HOUR IS AGAIN AVAILABLE IN THE SERVICE. 
    hour_availability = test_app.post("/hours/get", json=test_service_hours)
    hours = hour_availability.json().get("data")["hours"]
    i = 0
    hours_id = 0
    for hour in hours:
        i += 1
        if(hour["timeStart"] == test_reservation_to_cancel["timeStart"] and hour["timeEnd"] == test_reservation_to_cancel["timeEnd"]):
            print(i)
            hours_id = i

    if (hours_id == 0):
        fail(msg="elements not found")

    test_remove_hour = {
        "service_id": test_reservation_to_cancel["service_id"],
        "hour_id": hours[i-1]["hour_id"]
    }

    # REMOVE THE ADDED HOUR IN THE DB 
    remove_hour = test_app.post("/hours/update/remove", json=test_remove_hour)