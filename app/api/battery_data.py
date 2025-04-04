from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from uuid import uuid4

from app.core.db import get_db
from app.SQLAlchemy_models.battery import Battery
from app.schemas.battery_data import BatteryDataUpdate, BatterySchema
from app.SQLAlchemy_models.battery_history import BatteryHistory

# Setup logging
from app.core.logging import logger


router = APIRouter()


@router.get("/battery-count")
def battery_count(db: Session = Depends(get_db)):
    try:
        count = db.query(Battery).count()
        logger.info(f"Battery count retrieved: {count}")
        return {"count": count}
    except SQLAlchemyError as e:
        logger.exception("Database error while retrieving battery count")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/battery-data", response_model=BatterySchema)
def update_battery_data(data: BatteryDataUpdate, db: Session = Depends(get_db)):
    try:
        battery = db.query(Battery).filter(Battery.id == data.id).first()
        if not battery:
            logger.warning(f"Battery not found: {data.id}")
            raise HTTPException(status_code=404, detail="Battery not found")

        update_fields = data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(battery, field, value)

        now = datetime.now(timezone.utc)
        battery.last_updated = now
        battery.last_seen = now

        # Add a historical record
        history_entry = BatteryHistory(
            id=uuid4(),
            battery_id=battery.id,
            timestamp=now,
            state_of_charge=battery.state_of_charge,
            voltage=battery.voltage,
            temperature=battery.temperature,
            power_kw=battery.power_kw,
            status=battery.status,
            flag=battery.flag,
        )
        db.add(history_entry)
        db.commit()
        db.refresh(battery)

        logger.info(f"Battery data updated: {battery.identifier} (ID: {battery.id})")
        return battery

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"DB error during battery update for {data.id}")
        raise HTTPException(status_code=500, detail=f"Failed to update battery data: {str(e)}")
