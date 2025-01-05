import pytest
from fastapi.testclient import TestClient

def test_create_unit(client):
    unit_data = {
        "number": "101",
        "floor": 1,
        "area": 100.5,
        "building_id": 
    }
    response = client.post("/api/v1/units/", json=unit_data)
    assert response.status_code == 200
    assert response.json()["number"] == unit_data["number"]
