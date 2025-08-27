from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, db

router = APIRouter(prefix="/cat", tags=["Cats"])


@router.get("/breeds", response_model=List[schemas.BreedOut])
def list_breeds(db: Session = Depends(db.get_db)):
    return crud.list_breeds(db)


@router.get("/breeds/{breed_name}", response_model=schemas.BreedOut)
def get_breed(breed_name: str, db: Session = Depends(db.get_db)):
    return crud.get_breed_by_name(db, breed_name)


@router.post(
    "/breeds", response_model=schemas.BreedOut, status_code=status.HTTP_201_CREATED
)
def create_breed(payload: schemas.BreedCreate, db: Session = Depends(db.get_db)):
    return crud.create_breed(db, payload)


@router.patch("/breeds/{breed_name}", response_model=schemas.BreedOut)
def update_breed(
    breed_name: str, payload: schemas.BreedUpdate, db: Session = Depends(db.get_db)
):
    return crud.update_breed(db, breed_name, payload)


@router.delete("/breeds/{breed_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breed(breed_name: str, db: Session = Depends(db.get_db)):
    return crud.delete_breed(db, breed_name)
