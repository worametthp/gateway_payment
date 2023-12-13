from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from repositories import orders_repo
from schemas import orders_schema, products_schema,users_schema


routes = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    # dependencies=[Depends(JWTBearer())],
    responses={404: {"data": "not found!"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routes.post("/api/create_payment")
def create_payment(user: users_schema.UserBase, product: products_schema.ProductBase, db: Session = Depends(get_db)):
    try:
        order = orders_repo.create_payment(user, product, db)
        return {"status": True, "message": "created!", "data": order}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"status": False, "message": str(e), "data": None})


@routes.get("/get_payment_by_order_id")
def get_payment_by_order_id(orderid: str, db: Session):
    try:
        payment = orders_repo.get_payment_by_order_id(orderid, db)
        return {"status": True, "message": "get data completed!", "data": payment}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"status": False, "message": str(e), "data": None})

