
def test_forget_get_token(test_app):
    test_user = {
        "email": "forget@pwd.com",
    }

    response = test_app.post("/users/reset", json=test_user)
    assert response.status_code == 202
    assert response.json().get('message') == "Token generated successfully"

def test_forget_user_not_found(test_app):
    test_user = {
        "email": "nonexistent@user.com",
    }

    response = test_app.post("/users/reset", json=test_user)
    assert response.status_code == 404
    assert response.json().get('detail') == f"User with email {test_user['email']} not found"

def test_forget_bad_email(test_app):
    test_user = {
        "email": "nonexistent@",
    }

    response = test_app.post("/users/reset", json=test_user)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == "value is not a valid email address"

def test_forget_pwd_updated(test_app):
    test_user = {
        "token": "6087669ebec22e4193d6cd61",
        "new_password": "NewTestPassword1."
    }

    response = test_app.post("/users/reset/token", json=test_user)
    assert response.status_code == 200
    assert response.json().get('message') == "Resource updated successfully."

def test_forget_bad_token(test_app):
    test_user = {
        "token": "NotAToken",
        "new_password": "NewTestPassword1."
    }

    response = test_app.post("/users/reset/token", json=test_user)
    assert response.status_code == 404
    assert response.json().get('detail') == "Could not change password using provided token"

def test_forget_weak_pwd(test_app):
    test_user = {
        "token": "605e67283f5b377dfe2c1143",
        "new_password": "weak"
    }

    response = test_app.post("/users/reset/token", json=test_user)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == "Password must be 8 characters or longer"

def test_forget_missing_field(test_app):
    test_user = {
        "token": "605e67283f5b377dfe2c1143"
    }

    response = test_app.post("/users/reset/token", json=test_user)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == "field required"
