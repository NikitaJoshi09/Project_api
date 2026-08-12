from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from sqlmodel import SQLModel
from app.database import engine
from app.routres import product, auth
from app.models.product import Product
from app.models.user import User

app = FastAPI()

#DB Connection
@app.on_event("startup")
def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
        print("database connected successfully")
    except OperationalError as e:
        print("database connected failed",e)

@app.get("/")
def home():
    return {"message": "Product API is running"}

app.include_router(auth.router)
app.include_router(product.router)        