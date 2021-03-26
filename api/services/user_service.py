from fastapi import Request, HTTPException
from typing import Optional
from ..crud.user_crud import CRUDUser
from ..models import user_model

class UserService():
    async def get_user_by_id(request: Request, id: str) -> Optional[user_model.UserInDB]:
        retrieved_user = await CRUDUser.get_by_id(request, id)
        if not retrieved_user:
            raise HTTPException(
                status_code=404, 
                detail=f"User with ID {id} not found"
            )
        return retrieved_user

    async def get_user_by_email(request: Request, user_in: user_model.UserBase) -> Optional[user_model.UserInDB]:
        retrieved_user = await CRUDUser.get_by_email(request, user_in)
        if not retrieved_user:
            raise HTTPException(
                status_code=404,
                detail=f"User with email {user_in['email']} not found"
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
