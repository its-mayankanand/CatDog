import requests
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os

router = APIRouter(tags=["Dogs"])

DOG_API_URL = os.getenv("DOG_API_URL", "https://api.thedogapi.com/v1/images/search")


@router.get("/dog", response_class=HTMLResponse)
def get_dog():
    r = requests.get(DOG_API_URL, timeout=10)
    r.raise_for_status()
    return f"<img src='{r.json()[0]['url']}' alt='Dog Image'/>"
