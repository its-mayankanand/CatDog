from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

# Mock response for requests.get
mock_dog_response = [
    {"url": "https://example.com/fake-dog.jpg"}
]

def test_get_dog():
    with patch("app.api.dog.requests.get") as mock_get:
        # Configure mock to return the fake response
        mock_get.return_value.json.return_value = mock_dog_response
        mock_get.return_value.status_code = 200
        mock_get.return_value.raise_for_status = lambda: None  # does nothing

        response = client.get("/dog")

        assert response.status_code == 200
        assert "img" in response.text
        assert "https://example.com/fake-dog.jpg" in response.text
