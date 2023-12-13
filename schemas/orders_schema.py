from pydantic import BaseModel, Field
from uuid import UUID
from typing import Union


class OrderBase(BaseModel):
    fullname: str
    address: str
    order_id: UUID
    status: str
    session_id: str
    url: str


class OrderCreate(OrderBase):
    id: int


class Order(OrderBase):
    id: int


class ResultData(BaseModel):
    status: bool
    message: str
    data: Union[OrderBase, list[OrderBase], Order, int, str, None]


