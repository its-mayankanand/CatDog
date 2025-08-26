from fastapi.testclient import TestClient
from unittest.mock import patch
from unittest.mock import MagicMock

# 1) Prevent metadata.create_all
with patch("app.main.Base.metadata.create_all", lambda *a, **k: None):
    from app.main import app
    # 2) Override get_db just in case future routes touch DB
    from app.db import get_db
    def override_get_db():
        yield MagicMock()
    app.dependency_overrides[get_db] = override_get_db

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
