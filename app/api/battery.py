from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from uuid import UUID
from typing import List, Optional

from app.core.db import SessionLocal, get_db
from app.SQLAlchemy_models.battery import Battery
from app.SQLAlchemy_models.battery_history import BatteryHistory
from app.schemas.battery_data import BatteryCreate, BatterySchema
from app.core.logging import logger
from scripts.utils.archive_utils import archive_battery_history  # You'll create this


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/battery", response_model=BatterySchema, status_code=status.HTTP_201_CREATED)
def create_battery(battery: BatteryCreate, db: Session = Depends(get_db)):
    if battery.identifier:
        existing = db.query(Battery).filter(Battery.identifier == battery.identifier).first()
        if existing:
            logger.warning(f"Attempted to create duplicate identifier: {battery.identifier}")
            raise HTTPException(status_code=400, detail="Identifier already exists")

    try:
        new_battery = Battery(
            location=battery.location,
            capacity_kwh=battery.capacity_kwh,
            IP_address=battery.IP_address,
            postal_code=battery.postal_code,
            identifier=battery.identifier
        )
        db.add(new_battery)
        db.commit()
        db.refresh(new_battery)
        logger.info(f"Battery created successfully: {new_battery.identifier} (ID: {new_battery.id})")
        return new_battery
    except IntegrityError:
        db.rollback()
        logger.exception("Integrity error while creating battery")
        raise HTTPException(status_code=409, detail="Database integrity error — possibly duplicate field.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Database error while creating battery")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/battery/{battery_id}", response_model=BatterySchema)
def get_battery(battery_id: UUID, db: Session = Depends(get_db)):
    battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if not battery:
        logger.warning(f"Battery not found: {battery_id}")
        raise HTTPException(status_code=404, detail="Battery not found")
    logger.info(f"Battery retrieved: {battery.identifier} (ID: {battery.id})")
    return battery


@router.get("/batteries", response_model=List[BatterySchema])
def get_all_batteries(db: Session = Depends(get_db)):
    try:
        batteries = db.query(Battery).all()
        if not batteries:
            logger.info("No batteries found in database")
            raise HTTPException(status_code=404, detail="No batteries found")
        logger.info(f"{len(batteries)} batteries retrieved")
        return batteries
    except SQLAlchemyError as e:
        logger.exception("Database error while retrieving all batteries")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/battery", response_model=List[BatterySchema])
def get_batteries(location_prefix: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Battery)
        if location_prefix:
            logger.info(f"Filtering batteries with prefix: {location_prefix}")
            query = query.filter(Battery.identifier.ilike(f"{location_prefix}-%"))
        return query.all()
    except SQLAlchemyError as e:
        logger.exception("Database error while querying filtered batteries")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/batteries")
@router.delete("/battery/{battery_id}")
def delete_battery(
    battery_id: Optional[UUID] = None,
    delete_all: bool = Query(False, alias="all"),
    db: Session = Depends(get_db)
):
    try:
        if delete_all:
            batteries = db.query(Battery).all()
            for battery in batteries:
                archive_battery_history(battery.id, db)
                logger.info(f"Archiving battery history for {battery.identifier} (ID: {battery.id})")
                db.delete(battery) 
            db.commit()
            logger.warning(f"All batteries deleted after archiving")
            return {"detail": f"All batteries deleted"}
        
        if battery_id is None:
            raise HTTPException(status_code=400, detail="Missing battery_id")

        battery = db.query(Battery).filter(Battery.id == battery_id).first()
        if not battery:
            logger.warning(f"Battery not found: {battery_id}")
            raise HTTPException(status_code=404, detail="Battery not found")

        archive_battery_history(battery.id, db)
        logger.info(f"Archiving battery history for {battery.identifier} (ID: {battery.id})")
        db.delete(battery)
        db.commit()
        logger.info(f"Deleted battery {battery_id} after archiving")
        return {"detail": f"Battery {battery_id} deleted"}

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Error deleting battery")
        raise HTTPException(status_code=500, detail=f"Error deleting battery: {str(e)}")