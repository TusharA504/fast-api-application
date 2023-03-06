from pydantic import EmailStr, BaseModel, StrBytes, UUID4
from datetime import date
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    email: EmailStr
    is_active: bool
    id: UUID4

    class Config:
       
        orm_mode = True


class ItemCreate(BaseModel):
    title: str
    description: str


class ShowItem(BaseModel):
    id: UUID4
    title: str
    description: str
    date_posted: date

    class Config:
        orm_mode = True
