# create_db.py
from app.core.db import Base, engine
from app.models.battery import Battery

Base.metadata.create_all(bind=engine)
