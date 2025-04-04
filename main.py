from fastapi import FastAPI
from app.api import battery, battery_data

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Consus BMS API!"}


app.include_router(battery.router)
app.include_router(battery_data.router)

