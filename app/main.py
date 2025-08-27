# fastapi_app/main.py
from fastapi import FastAPI
from .db import Base, engine
from .api import cat, dog, health

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CatDog API", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to CatDog API"}


# include routers
app.include_router(cat.router)
app.include_router(dog.router)
app.include_router(health.router)
