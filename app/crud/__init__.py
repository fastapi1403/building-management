from crud.building import CRUDBuilding
from crud.floor import CRUDFloor
from models import Building, Floor

crud_building = CRUDBuilding(Building)
crud_floor = CRUDFloor(Floor)