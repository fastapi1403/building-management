from crud.building import CRUDBuilding
from crud.floor import CRUDFloor
from crud.owner import CRUDOwner
from models import Building, Floor, Owner

crud_building = CRUDBuilding(Building)
crud_floor = CRUDFloor(Floor)
crud_owner = CRUDOwner(Owner)