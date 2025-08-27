# this is unit test file for test_cat file 
from unittest.mock import patch
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# 1) Prevent metadata.create_all
with patch("app.main.Base.metadata.create_all", lambda *a, **k: None):
    from app.main import app

    # 2) Override get_db to avoid real DB session
    from app.db import get_db

    def override_get_db():
        yield MagicMock()

    app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_list_breeds():
    mock_breeds = [
        {
            "id": 1,
            "breed": "Persian",
            "origin": "India",
            "type": "Longhair",
            "body_type": "Cobby",
            "coat_type_length": "Long",
            "coat_pattern": "Solid",
            "image": "https://example.com/persian.jpg",
        },
        {
            "id": 3,
            "breed": "Siamese",
            "origin": "Thailand",
            "type": "Natural",
            "body_type": "Svelte",
            "coat_type_length": "Short",
            "coat_pattern": "Colorpoint",
            "image": "https://example.com/siamese.jpg",
        },
    ]

    with patch("app.api.cat.crud.list_breeds", return_value=mock_breeds):
        response = client.get("/cat/breeds")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["breed"] == "Persian"
        assert data[0]["origin"] == "India"
