# fastapi_app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

def list_breeds(db: Session):
    return db.query(models.CatBreed).order_by(models.CatBreed.breed.asc()).all()

def get_breed_by_name(db: Session, breed_name: str):
    breed = db.query(models.CatBreed).filter(models.CatBreed.breed.ilike(breed_name)).first()
    if not breed:
        raise HTTPException(status_code=404, detail=f"Breed '{breed_name}' not found")
    return breed

def create_breed(db: Session, payload: schemas.BreedCreate):
    exists = db.query(models.CatBreed).filter(models.CatBreed.breed.ilike(payload.breed)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Breed already exists")

    new_breed = models.CatBreed(**payload.model_dump())
    db.add(new_breed)

    try:
        db.commit()
        db.refresh(new_breed)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Breed already exists")
    return new_breed

def update_breed(db: Session, breed_name: str, payload: schemas.BreedUpdate):
    breed = get_breed_by_name(db, breed_name)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(breed, field, value)
    db.commit()
    db.refresh(breed)
    return breed

def delete_breed(db: Session, breed_name: str):
    breed = get_breed_by_name(db, breed_name)
    db.delete(breed)
    db.commit()
    return None

