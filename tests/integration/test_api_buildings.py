import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_building():
    response = client.post(
        "/api/v1/buildings/",
        json={
            "name": "Test Building",
            "address": "Test Address",
            "floors": 5,
            "units_count": 20
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Building"
