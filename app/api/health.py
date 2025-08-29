from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db import get_db
import logging               #1st change

logger = logging.getLogger(__name__)  #2nd change


router = APIRouter(tags=["Health"])


@router.get("/healthz")
def healthz(db: Session = Depends(get_db)):
    logger.info("Health check endpoint accessed")  #3rd change
    db.execute(text("SELECT 1"))
    logger.debug("Database health check query executed") 
    #4th change
    return {"status": "ok"}
