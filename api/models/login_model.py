from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.types import Optional
from .objectid_model import PyObjectId

class UserBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    email: EmailStr = Field(...) 
 
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": { 
                "email": "tim@apple.com"
            }
        }

class UserCheck(UserBase):
    password: str = Field(...)
    pwd_validate = validator('password', allow_reuse=True)
    class Config:
        schema_extra = {
            "example": { 
                "email": "tim@apple.com",
                "password": "SecretPwd1."
            }
        }

    
class UserUpdate(UserBase): 
    password: Optional[str] = None
    pwd_validate = validator('password', allow_reuse=True)

class UserLogin(UserBase):
    hashed_password: str = Field(...)
