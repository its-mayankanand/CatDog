from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
import requests
import socket

# ------------ Load env ------------
load_dotenv()

# ------------ FastAPI app ------------
app = FastAPI(title="CatDog API", version="1.0.0")

# ------------ Database setup (PostgreSQL) ------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://catuser:catpass@localhost:5432/catsdb"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     # helps avoid stale connections
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class CatBreed(Base):
    __tablename__ = "cat_breeds"
    id = Column(Integer, primary_key=True, index=True)
    # using generic String; change to Text if you expect long content
    breed = Column(String(200), unique=True, index=True, nullable=False)
    origin = Column(String(200))
    type = Column(String(200))
    body_type = Column(String(200))
    coat_type_length = Column(String(200))
    coat_pattern = Column(String(200))
    image = Column(String(500))  # can hold a URL or label

# Create the table(s) at startup if they don't exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------ Pydantic Schemas (Pydantic v2) ------------


class BreedBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    breed: str = Field(..., min_length=1, max_length=200, description="Breed name (unique)")
    origin: Optional[str] = Field(None, max_length=200)
    type: Optional[str] = Field(None, max_length=200)
    body_type: Optional[str] = Field(None, max_length=200)
    coat_type_length: Optional[str] = Field(None, max_length=200)
    coat_pattern: Optional[str] = Field(None, max_length=200)
    image: Optional[str] = Field(None, max_length=500)

class BreedCreate(BreedBase):
    pass


class BreedUpdate(BaseModel):
    """Used for partial updates (all fields optional)."""
    model_config = ConfigDict(from_attributes=True)

    breed: Optional[str] = Field(None, min_length=1, max_length=200, description="Breed name (unique)")
    origin: Optional[str] = Field(None, max_length=200)
    type: Optional[str] = Field(None, max_length=200)
    body_type: Optional[str] = Field(None, max_length=200)
    coat_type_length: Optional[str] = Field(None, max_length=200)
    coat_pattern: Optional[str] = Field(None, max_length=200)
    image: Optional[str] = Field(None, max_length=500)



class BreedOut(BreedBase):
    id: int

# ------------ image routes ------------
CAT_API_URL = os.getenv("CAT_API_URL", "https://api.thecatapi.com/v1/images/search")
DOG_API_URL = os.getenv("DOG_API_URL", "https://api.thedogapi.com/v1/images/search")

@app.get("/", response_class=HTMLResponse)
def read_root():
    hostname = socket.gethostname()
    return f"<h1>Hello from {hostname}!</h1>"

@app.get("/cat", response_class=HTMLResponse)
def get_cat():
    r = requests.get(CAT_API_URL, timeout=10)
    r.raise_for_status()
    image_url = r.json()[0]["url"]
    return f"<img src='{image_url}' alt='Cat Image'/>"

@app.get("/dog", response_class=HTMLResponse)
def get_dog():
    r = requests.get(DOG_API_URL, timeout=10)
    r.raise_for_status()
    image_url = r.json()[0]["url"]
    return f"<img src='{image_url}' alt='Dog Image'/>"

# ------------  Cat Breeds ------------

@app.get("/cat/breeds", response_model=List[BreedOut])
def list_breeds(db: Session = Depends(get_db)):
    return db.query(CatBreed).order_by(CatBreed.breed.asc()).all()


@app.get("/cat/breeds/{breed_name}", response_model=BreedOut)
def get_breed_by_name(breed_name: str, db: Session = Depends(get_db)):
    breed = db.query(CatBreed).filter(CatBreed.breed.ilike(breed_name)).first()
    if not breed:
        raise HTTPException(status_code=404, detail=f"Breed '{breed_name}' not found")
    return breed


@app.post("/cat/breeds", response_model=BreedOut, status_code=status.HTTP_201_CREATED)
def create_breed(payload: BreedCreate, db: Session = Depends(get_db)):
    # optional: check if exists (gives nicer error than IntegrityError)
    exists = db.query(CatBreed).filter(CatBreed.breed.ilike(payload.breed)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Breed already exists")

    new_breed = CatBreed(
        breed=payload.breed.strip(),
        origin=payload.origin,
        type=payload.type,
        body_type=payload.body_type,
        coat_type_length=payload.coat_type_length,
        coat_pattern=payload.coat_pattern,
        image=payload.image
    )

    db.add(new_breed)
    try:
        db.commit()
        db.refresh(new_breed)
    except IntegrityError:
        db.rollback()
        # Fall back in case of race conditions / uniqueness collisions
        raise HTTPException(status_code=400, detail="Breed already exists")
    return new_breed


@app.patch("/cat/breeds/{breed_name}", response_model=BreedOut)
def update_breed(breed_name: str, payload: BreedUpdate, db: Session = Depends(get_db)):
    breed = db.query(CatBreed).filter(CatBreed.breed.ilike(breed_name)).first()
    if not breed:
        raise HTTPException(status_code=404, detail=f"Breed '{breed_name}' not found")

    # Update only fields provided in the request
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(breed, field, value)

    db.commit()
    db.refresh(breed)
    return breed


@app.delete("/cat/breeds/{breed_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breed(breed_name: str, db: Session = Depends(get_db)):
    breed = db.query(CatBreed).filter(CatBreed.breed.ilike(breed_name)).first()
    if not breed:
        raise HTTPException(status_code=404, detail=f"Breed '{breed_name}' not found")

    db.delete(breed)
    db.commit()
    return None


# simple health check for DB connectivity
@app.get("/healthz")
def healthz(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


