# fastapi_app/models.py
from sqlalchemy import Column, Integer, String
from .db import Base

class CatBreed(Base):
    __tablename__ = "cat_breeds"

    id = Column(Integer, primary_key=True, index=True)
    breed = Column(String(200), unique=True, index=True, nullable=False)
    origin = Column(String(200))
    type = Column(String(200))
    body_type = Column(String(200))
    coat_type_length = Column(String(200))
    coat_pattern = Column(String(200))
    image = Column(String(500))
