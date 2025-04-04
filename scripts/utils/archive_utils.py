import os
import pandas as pd
from sqlalchemy.orm import Session
from app.SQLAlchemy_models.battery_history import BatteryHistory
from datetime import datetime


from global_var import ARCHIVE_EXPORT_PATH

#EXPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "archive"))
#os.makedirs(EXPORT_PATH, exist_ok=True)


def archive_battery_history(battery_id, db: Session):
    history = (
        db.query(BatteryHistory)
        .filter(BatteryHistory.battery_id == battery_id)
        .order_by(BatteryHistory.timestamp)
        .all()
    )
    if not history:
        return

    data = [h.__dict__.copy() for h in history]
    for entry in data:
        entry.pop("_sa_instance_state", None)

    df = pd.DataFrame(data)
    file_path = os.path.join(ARCHIVE_EXPORT_PATH, f"{battery_id}_history.csv")
    df.to_csv(file_path, index=False)
