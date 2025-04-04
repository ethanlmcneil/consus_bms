import os

API_BASE = "http://127.0.0.1:8000" # Assumes your FastAPI is running locally

ARCHIVE_EXPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "archive"))

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://consus_dev:consus@localhost:5432/consus_demo")
