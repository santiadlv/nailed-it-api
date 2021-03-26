from fastapi import Request, HTTPException
from typing import Optional
from ..crud.user_crud import CRUDUser
from ..models import user_model, login_model
from ..core import security

class UserService():
    async def get(request: Request, id: str) -> Optional[user_model.UserInDB]:
        retrieved_user = await CRUDUser.get_by_id(request, id)
        if not retrieved_user:
            raise HTTPException(
            status_code=404, 
            detail=f"User with ID {id} not found"
        )
        return retrieved_user

    async def create(request: Request, user_in: user_model.UserCreate) -> Optional[user_model.UserInDB]:
        existing_user = await CRUDUser.get_by_email(request, user_in)
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail=f"User with email {existing_user['email']} already exists in the system."
            )
        user = await CRUDUser.create(request, user_in)
        return user

    async def login(request: Request, user_login: login_model.UserCheck) -> Optional[login_model.UserLogin]:
        existing_user = await CRUDUser.get_by_email(request, user_login)
        if existing_user: 
            print("HELLO!")
            hashed_password = security.get_password_hash(user_login['password'])
            # hashed_password_original = security.get_password_hash(exi['password'])
            print(existing_user)

            if (security.authenticate(existing_user['hashed_password'], hashed_password)):
                print("HI!")

                return True
            else:
                raise HTTPException(
                    status_code=401,
                    detail=f"Incorrect password."
                )

        else:
            raise HTTPException(
                status_code=401,
                detail=f"The user with email {user_login['email']} does not exists in the system."
            )

