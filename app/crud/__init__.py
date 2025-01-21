from crud.building import CRUDBuilding
from crud.floor import CRUDFloor
from crud.owner import CRUDOwner
from crud.tenant import CRUDTenant
from crud.unit import CRUDUnit
from models import Building, Floor, Owner, Tenant, Unit

crud_building = CRUDBuilding(Building)
crud_floor = CRUDFloor(Floor)
crud_owner = CRUDOwner(Owner)
crud_tenant = CRUDTenant(Tenant)
crud_unit = CRUDUnit(Unit)