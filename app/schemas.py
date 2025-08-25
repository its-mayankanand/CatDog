# fastapi_app/schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class BreedBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    breed: str = Field(..., min_length=1, max_length=200)
    origin: Optional[str] = None
    type: Optional[str] = None
    body_type: Optional[str] = None
    coat_type_length: Optional[str] = None
    coat_pattern: Optional[str] = None
    image: Optional[str] = None

class BreedCreate(BreedBase):
    pass

class BreedUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    breed: Optional[str] = None
    origin: Optional[str] = None
    type: Optional[str] = None
    body_type: Optional[str] = None
    coat_type_length: Optional[str] = None
    coat_pattern: Optional[str] = None
    image: Optional[str] = None

class BreedOut(BreedBase):
    id: int
