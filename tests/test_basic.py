from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import os

# Force SQLite for this test module before importing app.main
os.environ["DATABASE_URL_LOCAL"] = "sqlite+pysqlite:///:memory:"

# Prevent metadata.create_all from touching any real DB at import
with patch("app.main.Base.metadata.create_all", lambda *a, **k: None):
    from app.main import app
    from app.db import get_db
    def override_get_db():
        yield MagicMock()
    app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CatDog API"}

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


