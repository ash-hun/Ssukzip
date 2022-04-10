from typing import List, Optional

from pydantic import BaseModel # 객체 타입설정

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool


    class Config:
        orm_mode = True