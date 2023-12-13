from pydantic import BaseModel

class OrderBase(BaseModel):
    fullname: str
    address: str
    order_id: str
    status: str
    session_id: str


class OrderCreate(OrderBase):
    id: int


class ResultData(BaseModel):
    status: bool
    message: str
    data: list[OrderBase]


