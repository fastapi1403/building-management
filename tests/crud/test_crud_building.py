import pytest
from src.crud.crud_building import crud_building
from src.schemas.building import BuildingCreate

@pytest.mark.asyncio
async def test_create_building(test_db):
    building_in = BuildingCreate(
        name="Test Building",
        address="123 Test St",
        floors=5,
        units_count=20
    )
    building = await crud_building.create(test_db, obj_in=building_in)
    assert building.name == building_in.name
    assert building.address == building_in.address
