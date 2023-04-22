from typing import Union, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


class PrivateMessage(BaseModel):
    id: int
    from_userid: int
    to_userid: int
    subject: str
    message: str
    folder: str
    unread: str

    class Config:
        orm_mode = True


class PrivateMessageCreate(BaseModel):
    from_userid: int
    to_userid: int
    subject: str
    message: str

class PrivateMessageUpdate(BaseModel):
    message_id_list: list[int]
    read: Optional[str] = None
    trash: Optional[str] = None
    spam: Optional[str] = None

class PrivateMessageFolderUpdate(BaseModel):
    id: int
    folder: str
