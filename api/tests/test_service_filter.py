from fastapi import status

def test_filter_services_success(test_app):
    test_categories = {
        "categories": ["Nails", "Tanning"]
    }

    response = test_app.post("/services/filter", json=test_categories)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('message') == "List of filtered services retrieved successfully"

def test_filter_no_services_in_category(test_app):
    test_categories = {
        "categories": ["Complementary care"]
    }

    response = test_app.post("/services/filter", json=test_categories)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == "Services with specified category/categories could not be found"

def test_filter_services_validation_error_empty(test_app):
    test_categories = {
        "categories": []
    }

    response = test_app.post("/services/filter", json=test_categories)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json().get('detail')[0]['msg'] == "Categories list cannot be empty"

def test_filter_services_validation_error_not_a_category(test_app):
    test_categories = {
        "categories": ["wrong"]
    }

    response = test_app.post("/services/filter", json=test_categories)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert [response.json().get('detail')[0]['msg']] == [f"Category '{category}' does not exist" for category in test_categories["categories"]]

def test_filter_services_validation_error_field_required(test_app):
    test_categories = {}

    response = test_app.post("/services/filter", json=test_categories)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json().get('detail')[0]['msg'] == "field required"
