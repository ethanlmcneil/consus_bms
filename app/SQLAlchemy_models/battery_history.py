# app/SQLAlchemy_models/battery_history.py
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from app.core.db import Base

class BatteryHistory(Base):
    __tablename__ = "battery_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    battery_id = Column(UUID(as_uuid=True), ForeignKey("batteries.id"), nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)

    state_of_charge = Column(Float)
    status = Column(String)
    flag = Column(String)
    power_kw = Column(Float)
    voltage = Column(Float)
    temperature = Column(Float)

    battery = relationship("Battery", back_populates="history")
