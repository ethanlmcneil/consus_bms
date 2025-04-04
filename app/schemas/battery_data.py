from decimal import Decimal
from pydantic import BaseModel, Field, constr, condecimal
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing_extensions import Annotated
from pydantic import IPvAnyAddress


# Enums for status and flag
class BatteryStatus(str, Enum):
    idle = "idle"
    charging = "charging"
    discharging = "discharging"

class BatteryFlag(str, Enum):
    ok = "ok"
    warning = "warning"
    error = "error"


# Create schema with constraints
class BatteryCreate(BaseModel):
    location: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]
    capacity_kwh: Annotated[Decimal, condecimal(gt=0, lt=1000)]
    IP_address: Optional[str] = None
    postal_code: Optional[str] = None
    identifier: Optional[Annotated[str, constr(max_length=50)]] = None

    class Config:
        from_attributes = True


# Update schema for dynamic data
class BatteryDataUpdate(BaseModel):
    id: UUID
    state_of_charge: Optional[Annotated[Decimal, condecimal(ge=0, le=100)]] = None
    flag: Optional[BatteryFlag] = None
    status: Optional[BatteryStatus] = None
    power_kw: Optional[float] = Field(None, ge=0)
    voltage: Optional[float] = Field(None, ge=0)
    temperature: Optional[float] = Field(ge=-50, le=100)  # Sensible range

# Output schema for API responses
class BatterySchema(BaseModel):
    id: UUID
    identifier: Optional[str]
    IP_address: Optional[str]
    location: str
    capacity_kwh: float
    postal_code: Optional[str]
    state_of_charge: Optional[float]
    status: Optional[BatteryStatus]
    flag: Optional[BatteryFlag]
    power_kw: Optional[float]
    voltage: Optional[float]
    temperature: Optional[float]
    last_updated: Optional[datetime]
    last_seen: Optional[datetime]

    class Config:
        from_attributes = True
