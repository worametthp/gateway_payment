from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases.database import engine
from models import model
from routes.orders_route import routes as orders_router
import sqlalchemy


model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(orders_router)

@app.get("/")
def hello():
    return {"hello": "Gateway Payment"}


