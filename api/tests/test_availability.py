from fastapi import status

def test_get_hour_availability_success(test_app):
    test_identifier = {
        "service_id": "60866216a23cc075ce72ee8b"
    }

    response = test_app.post("/hours/get", json=test_identifier)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("message") == "Availability hours retrieved successfully"
    assert "hours" in response.json().get("data")

def test_get_hour_availability_not_found(test_app):
    test_identifier = {
        "service_id": "TEST-ID"
    }

    response = test_app.post("/hours/get", json=test_identifier)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.json().get("detail") == "Availability hours for service with ID TEST-ID could not be found"

def test_update_availability_success(test_app):
    test_identifier = {
        "service_id": "60866216a23cc075ce72ee8b"
    }

    response1 = test_app.post("/hours/get", json=test_identifier)
    assert response1.status_code == status.HTTP_200_OK
    original_hours = response1.json().get("data")["hours"]

    test_hours = {
        "service_id": "60866216a23cc075ce72ee8b",
        "hours": [
            {
                "timeStart": 0,
                "timeEnd": 1439
            }
        ]
    }

    response2 = test_app.post("/hours/update", json=test_hours)
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json().get("message") == "Service's availability hours updated successfully"

    original = {
        "service_id": "60866216a23cc075ce72ee8b",
        "hours": original_hours
    }

    response3 = test_app.post("/hours/update", json=original)
    assert response3.status_code == status.HTTP_200_OK
    assert response3.json().get("data")["hours"] == original_hours

def test_update_availability_failure(test_app):
    test_hours = {
        "service_id": "TEST-ID",
        "hours": [
            {
                "timeStart": 0,
                "timeEnd": 1439
            }
        ]
    }

    response2 = test_app.post("/hours/update", json=test_hours)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert response2.json().get("detail") == "Availability hours for service with ID TEST-ID could not be updated"

def test_add_hour_to_and_remove_hour_from_availability_success(test_app):
    test_hour_add = {
        "service_id": "60866216a23cc075ce72ee8b",
        "timeStart": 0,
        "timeEnd": 1439
    }

    response1 = test_app.post("/hours/update/add", json=test_hour_add)
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json().get("message") == "Successfully added an hour to the service's availability"

    test_hour_remove = {
        "service_id": "60866216a23cc075ce72ee8b",
        "hour_id": response1.json().get("data")["hours"][0]["hour_id"]
    }

    response2 = test_app.post("/hours/update/remove", json=test_hour_remove)
    assert response2.status_code == status.HTTP_202_ACCEPTED
    assert response2.json().get("message") == "Successfully removed an hour from the service's availability"

def test_add_hou_to_and_remove_hour_from_availability_failure(test_app):
    test_hour_add = {
        "service_id": "TEST-ID",
        "timeStart": 0,
        "timeEnd": 1439
    }

    response1 = test_app.post("/hours/update/add", json=test_hour_add)
    assert response1.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response1.json().get("detail") == "Availability hours for service with ID TEST-ID could not be found"

    test_hour_remove = {
        "service_id": "TEST-ID",
        "hour_id": "FAKE-HOUR-ID"
    }

    response2 = test_app.post("/hours/update/remove", json=test_hour_remove)
    assert response2.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response2.json().get("detail") == "Availability hours for service with ID TEST-ID could not be found"

def test_remove_hour_from_availability_bad_hour_id(test_app):
    test_hour_remove = {
        "service_id": "60866216a23cc075ce72ee8b",
        "hour_id": "BAD-HOUR-ID"
    }

    response = test_app.post("/hours/update/remove", json=test_hour_remove)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.json().get("detail") == "Hour with ID BAD-HOUR-ID could not be found in service"
