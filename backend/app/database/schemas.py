from pydantic import BaseModel, EmailStr
import typing as t


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



class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class UserOut(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
