from fastapi import status

def test_get_service_price_by_id(test_app):
    test_identifier = {
        "id": "608608d7041aa13d76554244"
    }

    response = test_app.post("/services/price", json=test_identifier)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('message') == "Service price retrieved successfully"
    assert response.json().get('data')['price'] == "500.00"

def test_get_price_of_non_existent_service(test_app):
    test_identifier = {
        "id": "this is not a service ID"
    }

    response = test_app.post("/services/price", json=test_identifier)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == "Price for selected service not found"

def test_get_service_price_wrong_validation(test_app):
    test_identifier = {
        "wrong_key": "test_data"
    }

    response = test_app.post("/services/price", json=test_identifier)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json().get('detail')[0]['msg'] == "field required"
    assert response.json().get('detail')[0]['type'] == "value_error.missing"
