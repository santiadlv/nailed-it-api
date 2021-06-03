from ..core import settings

"""""""""""""""""""""""""""""""""
VALID USER INSIDE DB
{
  "username": "Tim Cook",
  "email": "someemail@gmail.com",
  "password": "FooBarPass"
}

"""""""""""""""""""""""""""""""""

# SUCCESFUL LOGIN, WITH NO ERRORS
def test_user_login(test_app):
    user_credentials={
        "email": "someemail@gmail.com", 
        "password": "FooBarPass"
    }

    response = test_app.post(
        "/users/login",
        json=user_credentials
    )
    assert response.status_code == 200
    assert response.json().get('messsage') == "Login Succesful"
    assert response.json().get('data')['authentication'] == True

# INCORRECT PASSWORD, BUT A VALID EMAIL IN THE SYSTEM
def test_user_login_incorrect_password(test_app):
    user_credentials={
        "email": "someemail@gmail.com", 
        "password": "incorrectPassword"
    }

    response = test_app.post(
        "/users/login",
        json=user_credentials
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect password."
    }

# INCORRECT PASSWORD, BUT A VALID EMAIL IN THE SYSTEM
def test_user_login_invalid_email(test_app):
    user_credentials={
        "email": "some_incorrect_email@gmail.com", 
        "password": "FooBarPass"
    }

    response = test_app.post(
        "/users/login",
        json=user_credentials
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "The user with email some_incorrect_email@gmail.com does not exists in the system."
    }

# WEAK PASSWORD ENTERED
def test_login_weak_password(test_app):
    user_credentials={
        "email": "someemail@gmail.com", 
        "password": "weak"
    }

    response = test_app.post("/users/login", json=user_credentials)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == "Password must be 8 characters or longer"

# EMPTY USERNAME ENTERED
def test_login_empty_username(test_app):
    user_credentials={
        "email": "", 
        "password": "FooBarPass"
    }

    response = test_app.post("/users/login", json=user_credentials)
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == "value is not a valid email address"