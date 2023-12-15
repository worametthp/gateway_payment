from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases.database import engine
from models import model
from routes.orders_route import routes as orders_router
import sqlalchemy
import json
import os
import stripe
from flask import Flask, jsonify, request
import uvicorn

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(orders_router)

@app.get("/")
def hello():
    return {"hello": "Gateway Payment"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)




