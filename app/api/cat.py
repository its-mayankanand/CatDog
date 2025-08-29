from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, db
import logging     #1st change

logger = logging.getLogger(__name__) #2nd change

router = APIRouter(prefix="/cat", tags=["Cats"])


@router.get("/breeds", response_model=List[schemas.BreedOut])
def list_breeds(db: Session = Depends(db.get_db)):
    logger.info("Listing all cat breeds") #3rd change
    breeds = crud.list_breeds(db)
    logger.debug(f"Returned {len(breeds)} breeds") #4th change
    return breeds


@router.get("/breeds/{breed_name}", response_model=schemas.BreedOut)
def get_breed(breed_name: str, db: Session = Depends(db.get_db)):
    logger.info(f"fetching breed: {breed_name}")  #5th change
    return crud.get_breed_by_name(db, breed_name)


@router.post(
    "/breeds", response_model=schemas.BreedOut, status_code=status.HTTP_201_CREATED
)
def create_breed(payload: schemas.BreedCreate, db: Session = Depends(db.get_db)):
    logger.info(f"Creating breed: {payload.breed}")  #6th change
    return crud.create_breed(db, payload)


@router.patch("/breeds/{breed_name}", response_model=schemas.BreedOut)
def update_breed(
    breed_name: str, payload: schemas.BreedUpdate, db: Session = Depends(db.get_db)
):
    logger.info(f"Updating breed: {breed_name}") #7th change
    return crud.update_breed(db, breed_name, payload)


@router.delete("/breeds/{breed_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breed(breed_name: str, db: Session = Depends(db.get_db)):
    logger.info(f"Deleting breed: {breed_name}")  #8th change
    return crud.delete_breed(db, breed_name)
