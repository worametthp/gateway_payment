from sqlalchemy import Boolean, String, Integer, DateTime, Date, Column, NVARCHAR, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from databases.database import Base


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    address = Column(String)
    order_id = Column(String)
    status = Column(String)
    session_id = Column(String)
    url = Column(String)


