from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.types import Optional
from .objectid_model import PyObjectId


def password_strength_check(value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password must be 8 characters or longer')
        return value

class UserBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    email: EmailStr = Field(...)
    username: str = Field(...)

    @validator('username')
    def check_name_not_empty(cls, value: str) -> str:
        assert value != "", 'Empty strings are not allowed'
        return value

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Tim Cook",
                "email": "tim@apple.com"
            }
        }

class UserCreate(UserBase):
    password: str = Field(...)
    pwd_validate = validator('password', allow_reuse=True)(password_strength_check)
    class Config:
        schema_extra = {
            "example": {
                "username": "Tim Cook",
                "email": "tim@apple.com",
                "password": "SecretPwd1."
            }
        }

    
class UserUpdate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    pwd_validate = validator('password', allow_reuse=True)(password_strength_check)

class UserInDB(UserBase):
    hashed_password: str = Field(...)
