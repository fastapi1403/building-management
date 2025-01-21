from crud.building import CRUDBuilding
from crud.floor import CRUDFloor
from crud.owner import CRUDOwner
from crud.tenant import CRUDTenant
from models import Building, Floor, Owner, Tenant

crud_building = CRUDBuilding(Building)
crud_floor = CRUDFloor(Floor)
crud_owner = CRUDOwner(Owner)
crud_tenant = CRUDTenant(Tenant)