from typing import Optional
from ..crud import user_crud
from ..models import user_model
from fastapi import HTTPException

class UserService():
    def create(user_in: user_model.UserCreate) -> Optional[user_model.UserGet]:
        existing_user = user_crud.CRUDUser.get_by_email(email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="The user with this email already exists in the system."
            )
        user = user_crud.CRUDUser.create(obj_in=user_in)
        return user
