import pytest
from src.crud.crud_unit import crud_unit
from src.schemas.unit import UnitCreate

@pytest.mark.asyncio
async def test_create_unit(test_db):
    unit_in = UnitCreate(
        number="101",
        floor=1,
        area=100.5,
        bedrooms=2,
        building_id=
    )
    unit = await crud_unit.create(test_db, obj_in=unit_in)
    assert unit.number == unit_in.number
    assert unit.floor == unit_in.floor
