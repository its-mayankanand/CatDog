from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

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
