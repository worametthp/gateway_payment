from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import orders_schema, users_schema , products_schema
from models import model
import stripe
import uuid


stripe.api_key = "sk_test_51OMZ7hFCgtxx1L6a5RMQSF70rEDo1GUHLgtNt0E6BzyOIMv9PTUufghE9SAlZFJKYVohla4zKogmsHtuDi9rokrZ00KtjY8TV9"


def create_payment(user: users_schema.UserBase, product: products_schema.ProductBase, db: Session):
    try:
        orderId = uuid.uuid4()
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "thb",
                        "product_data": {
                            "name": product.name
                        },
                        "unit_amount": product.price * 100
                    },
                    "quantity": product.quantity,
                },
            ],
            mode='payment',
            success_url=f'http://localhost:8000/success.html?id={orderId}',
            cancel_url=f'http://localhost:8000/cancel.html?id={orderId}'
        )
        orders = {
            'fullname': user.fullname,
            'address': user.address,
            'order_id': orderId,
            'session_id': checkout_session.id,
            'status': checkout_session.status
        }
        create_order = model.Orders(**orders)
        db.add(create_order)
        db.commit()
        db.refresh(create_order)
        return orders_schema.OrderBase(**orders)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not create")


def get_payment_by_order_id(orderid: str, db: Session):
    payment = db.query(model.Orders).filter_by(order_id=orderid).first()
    if payment:
        return payment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment Not Found")

