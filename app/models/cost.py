from typing import Optional
from enum import Enum
from datetime import date
from sqlmodel import SQLModel, Field
from . import TimeStampModel


class CostType(str, Enum):
    GAS = "gas"
    WATER = "water"
    ELECTRICITY = "electricity"
    CLEANING = "cleaning"
    REPAIR = "repair"
    MAINTENANCE = "maintenance"
    MISCELLANEOUS = "miscellaneous"


class DivisionMethod(str, Enum):
    PER_UNIT = "per_unit"
    PER_PERSON = "per_person"
    PER_AREA = "per_area"
    CUSTOM = "custom"


class Cost(TimeStampModel, table=True):
    __tablename__ = "costs"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: CostType
    amount: float
    date: date
    description: str
    division_method: DivisionMethod
    is_warm_month: bool = Field(default=True)
    assigned_to_owner: bool = Field(default=False)
    custom_division_rules: Optional[dict] = Field(default=None)
