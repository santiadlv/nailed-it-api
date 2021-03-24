from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from pydantic.types import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserIn(UserBase):
    password: str

    @validator('password')
    def password_strength_check(cls, value):
        if len(value) < 8:
            raise ValueError('Password ust be 8 characters or longer')
        return value

class UserOut(UserBase):
    pass

class UserInDB(BaseModel):
    hashed_password: str

