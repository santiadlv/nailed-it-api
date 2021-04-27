from fastapi import status

def test_get_error_when_invalid_id(test_app):
    id = "this_is_not_id"
    response = test_app.get(f"/salons/{id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == f"Salon with ID {id} not found"
