from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class Battery(Base):

    __tablename__ = "batteries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4) # random identifier
    identifier = Column(String, unique=True) # readable identifier
    postal_code = Column(String)
    IP_address = Column(String, unique=True)

    location = Column(String, nullable=False)
    capacity_kwh = Column(Float, nullable=False)

    state_of_charge = Column(Float)
    status = Column(String)  # idle, charging, discharging
    flag = Column(String)  # ok, warning, error
    last_updated = Column(DateTime, default=datetime.now(timezone.utc)
)

   
    power_kw = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    last_seen = Column(DateTime, default=datetime.now(timezone.utc)
)
    # app/SQLAlchemy_models/battery.py
    history = relationship("BatteryHistory", back_populates="battery", cascade="all, delete-orphan")
