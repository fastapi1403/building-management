import pytest
from fastapi.testclient import TestClient
from src.schemas.building import BuildingCreate

def test_create_building(client):
    building_data = {
        "name": "Test Building",
        "address": "123 Test St",
        "floors": 5,
        "units_count": 20
    }
    response = client.post("/api/v1/buildings/", json=building_data)
    assert response.status_code == 200
    assert response.json()["name"] == building_data["name"]
