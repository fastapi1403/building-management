from src.schemas.unit import UnitCreate

def test_create_unit(test_client: TestClient):
    unit_data = {
        "number": "101",
        "floor": 1,
        "area": 100.5,
        "bedrooms": 2,
        "building_id": 
    }
    response = test_client.post("/api/v1/units/", json=unit_data)
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == unit_data["number"]
