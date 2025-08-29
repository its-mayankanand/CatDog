# fastapi_app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas
import logging #1st change

#2nd change
logger = logging.getLogger(__name__)

def list_breeds(db: Session):
    logger.info("Querying all cat breeds from database") #3rd change
    return db.query(models.CatBreed).order_by(models.CatBreed.breed.asc()).all()


def get_breed_by_name(db: Session, breed_name: str):
    logger.info(f"Querying cat breed by name: {breed_name}") #4th change
    breed = (
        db.query(models.CatBreed)
        .filter(models.CatBreed.breed.ilike(breed_name))
        .first()
    )
    if not breed:
        logger.warning(f"Breed '{breed_name}' not found") 
        #5th change
        raise HTTPException(status_code=404, detail=f"Breed '{breed_name}' not found")
    return breed


def create_breed(db: Session, payload: schemas.BreedCreate):
    logger.info(f"Attempting to create breed:{payload.breed}")
    #6th change
    exists = (
        db.query(models.CatBreed)
        .filter(models.CatBreed.breed.ilike(payload.breed))
        .first()
    )
    if exists:
        logger.warning("Breed already exists")
        #7th change
        raise HTTPException(status_code=400, detail="Breed already exists")

    new_breed = models.CatBreed(**payload.model_dump())
    db.add(new_breed)

    try:
        db.commit()
        db.refresh(new_breed)
        logger.info(f"Breed '{payload.breed}' created successfully") #8th change
    except IntegrityError:
        db.rollback()
        logger.error("Integrity error: Breed already exists") #9th change
        raise HTTPException(status_code=400, detail="Breed already exists")
    return new_breed


def update_breed(db: Session, breed_name: str, payload: schemas.BreedUpdate):
    logger.info(f"Updating breed: {breed_name}") #10th change
    breed = get_breed_by_name(db, breed_name)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(breed, field, value)
    db.commit()
    db.refresh(breed)
    logger.info(f"Breed '{breed_name}' updated successfully") #11th change
    return breed


def delete_breed(db: Session, breed_name: str):
    logger.info(f"Deleting breed: {breed_name}") #12th change
    breed = get_breed_by_name(db, breed_name)
    db.delete(breed)
    db.commit()
    logger.info(f"Breed '{breed_name}' deleted successfully") #13th change
    return None


