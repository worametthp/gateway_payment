from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import orders_schema, users_schema, products_schema
from models import model
import stripe
import uuid
import json
import os
from flask import Flask, jsonify, request


stripe.api_key = "sk_test_51OMZ7hFCgtxx1L6a5RMQSF70rEDo1GUHLgtNt0E6BzyOIMv9PTUufghE9SAlZFJKYVohla4zKogmsHtuDi9rokrZ00KtjY8TV9"
endpoint_secret = 'whsec_b7762bdc5c2a9212fffc3a8fa22025b97c1052dd03f6b78a814c66ae9277c8af'

def create_payment(user: users_schema.UserBase, product: products_schema.ProductBase, db: Session):
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
        'status': checkout_session.status,
        'url': checkout_session.url
    }
    create_order = model.Orders(**orders)
    db.add(create_order)
    db.commit()
    db.refresh(create_order)
    return orders_schema.OrderBase(**orders)


def get_payment_by_order_id(orderid: str, db: Session):
    payment = db.query(model.Orders).filter_by(order_id=orderid).first()
    if payment:
        return payment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment Not Found")


def webhook(db: Session):
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.completed':
      payment_intent = event['data']['object']
      sessionId = payment_intent.id
      db.query(model.Orders).filter_by(session_id=sessionId).update({'status': payment_intent.stutus})
      db.commit()
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)