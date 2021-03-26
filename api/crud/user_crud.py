from typing import Optional
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import user_model
from ..core.security import get_password_hash
from ..core import settings

class CRUDUser():
    async def get_by_email(request: Request, user_in: user_model.UserCreate) -> Optional[user_model.UserInDB]:
        if (user := await request.app.mongodb[settings.MONGODB_COLLECTION].find_one({"email": user_in['email']})) is not None:
            return user
        else: return None

    async def get_by_id(request: Request, id: str) -> Optional[user_model.UserInDB]:
        if (user := await request.app.mongodb[settings.MONGODB_COLLECTION].find_one({"_id": id})) is not None:
            return user
        else: return None

    async def create(request: Request, obj_in: user_model.UserCreate) -> Optional[user_model.UserInDB]:
        new_user = user_model.UserInDB(
            email=obj_in['email'],
            username=obj_in['username'],
            hashed_password=get_password_hash(obj_in['password'])
        )
        serialized_user = jsonable_encoder(new_user)
        new_user = await request.app.mongodb[settings.MONGODB_COLLECTION].insert_one(serialized_user)
        return serialized_user

    async def delete(request: Request, obj_in: user_model.UserLogin) -> Optional[user_model.UserLogin]:
        if (result := await request.app.mongodb[settings.MONGODB_COLLECTION].find_one_and_delete({"email": obj_in['email']})) is not None:
            serialized_user = jsonable_encoder(result)
            return serialized_user
        else: return None
