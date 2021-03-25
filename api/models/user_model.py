from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from pydantic.types import Optional


def password_strength_check(value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password ust be 8 characters or longer')
        return value

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

    pwd_validate = validator('password', allow_reuse=True)(password_strength_check)
    
class UserUpdate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None

    pwd_validate = validator('password', allow_reuse=True)(password_strength_check)

class UserGet(UserBase):
    email: EmailStr
    username: str

class UserInDB(UserBase):
    key: Optional[str]
    hashed_password: str
