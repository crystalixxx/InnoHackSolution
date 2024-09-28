from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    email: str = None


class UserBase(BaseModel):
    email: EmailStr
    name: str
    username: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str
