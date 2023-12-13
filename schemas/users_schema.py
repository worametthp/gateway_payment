from pydantic import BaseModel


class UserBase(BaseModel):
    fullname: str
    address: str

