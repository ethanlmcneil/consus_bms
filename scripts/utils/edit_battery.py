import requests
import random
from uuid import UUID
import time

API_BASE = "http://127.0.0.1:8000"

def fake_update_all_batteries():
    while True:
        response = requests.get(f"{API_BASE}/batteries")
        if response.status_code == 200:
            battery_ids = [UUID(battery["id"]) for battery in response.json()]
            for battery_id in battery_ids:
                data = {
                    "id": str(battery_id),
                    "state_of_charge": round(random.uniform(40, 60), 2),
                    "temperature": round(random.uniform(20, 30), 1),
                    "status": "charging"
                }
                r = requests.post(f"{API_BASE}/battery-data", json=data)
                #print(f"Battery {battery_id}: {r.status_code}, {r.text}")
        else:
            print(f"Failed to fetch batteries: {response.status_code}, {response.text}")
        time.sleep(20)



