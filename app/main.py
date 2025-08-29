# fastapi_app/main.py
import logging                        #1st change
from fastapi import FastAPI
from .db import Base, engine
from .api import cat, dog, health

#2nd change
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="CatDog API", version="1.0.0")

#3rd change
logger.info("Starting CatDog API application")


@app.get("/")
def read_root():
    return {"message": "Welcome to CatDog API"}

# include routers
app.include_router(cat.router)
app.include_router(dog.router)
app.include_router(health.router)
