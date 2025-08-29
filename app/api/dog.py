import requests
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os
import logging     #1st change

logger = logging.getLogger(__name__)  #2nd change

router = APIRouter(tags=["Dogs"])

DOG_API_URL = os.getenv("DOG_API_URL", "https://api.thedogapi.com/v1/images/search")


@router.get("/dog", response_class=HTMLResponse)
def get_dog():
    logger.info("Fetching dog image from external API")  #3rd change
    r = requests.get(DOG_API_URL, timeout=10)
    r.raise_for_status()
    logger.debug(f"Dog API response: {r.json()}")
    return f"<img src='{r.json()[0]['url']}' alt='Dog Image'/>"
