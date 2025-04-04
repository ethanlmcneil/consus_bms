from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from global_var import DATABASE_URL
# configures the database connection from .env file

#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://consus_dev:consus@localhost:5432/consus_demo")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
