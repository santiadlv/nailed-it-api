from typing import Optional
from deta import Deta
from ..core import settings
from fastapi.encoders import jsonable_encoder
from ..models import user_model
from ..core.security import get_password_hash

deta = Deta(settings.DETA_PROJECT_KEY)
db = deta.Base(settings.DETA_DB)

class CRUDUser():
    def get_by_email(email: str) -> Optional[user_model.UserInDB]:
        user = next(db.fetch({"email" : email}))
        return user

    def create(obj_in: user_model.UserCreate) -> Optional[user_model.UserGet]:
        new_user = user_model.UserInDB(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
        )
        serialized_user = jsonable_encoder(new_user)
        db.put(serialized_user)
        return new_user
