def test_delete_success(test_app):
    test_user1 = {
        "username": "Test User",
        "email": "test@email.com",
        "password": "TestPassword."
    }

    response1 = test_app.post("/users/signup", json=test_user1)
    assert response1.status_code == 201

    test_user2 = {
        "email": "test@email.com",
        "password": "TestPassword."
    }

    response2 = test_app.delete("/users/delete", json=test_user2)
    assert response2.status_code == 200
    assert response2.json().get('message') == "Account Deleted"

def test_delete_email_not_exists(test_app):
    test_user = {
        "username": "Test User",
        "email": "test@email.com",
        "password": "TestPassword."
    }

    response = test_app.post("/users/signup", json=test_user)
    assert response.status_code == 201

    test_user = {
        "email": "notexists@email.com",
        "password": "TestPassword."
    }

    response = test_app.delete("/users/delete", json=test_user)
    assert response.status_code == 401
    assert response.json().get('detail') == f"The user with email {test_user['email']} does not exists in the system."

def test_delete_missing_field(test_app):
    test_user = {
        "email": "test@user.com"
    }

    response = test_app.delete("/users/delete", json=test_user)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == "field required"
