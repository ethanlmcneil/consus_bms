import requests
import random
import time

from cems.scripts.utils.creation_funcs import create_identifier
from app.core.logging import logger  # central logger

API_BASE = "http://127.0.0.1:8000"  # Assumes your FastAPI is running locally


def add_battery(location: str, capacity: float, IP_address: str, postal_code: str) -> str:
    identifier = create_identifier(postal_code, capacity)
    logger.info(f"Creating battery with identifier={identifier}, location={location}, capacity={capacity}")

    try:
        response = requests.post(
            f"{API_BASE}/battery",
            json={
                "location": location,
                "capacity_kwh": capacity,
                "IP_address": IP_address,
                "identifier": identifier,
                "postal_code": postal_code
            }
        )

        if response.status_code == 200:
            battery = response.json()
            logger.info(f"Battery created: {battery}")
            return battery["id"]
        else:
            logger.error(f"Failed to create battery: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        logger.exception(f"Error creating battery: {str(e)}")
        return None


def delete_batteries(battery_ids: list, delete_all: bool = False):
    """
    Deletes batteries from the database.

    :param battery_ids: List of battery UUIDs to delete.
    :param delete_all: If True, deletes all batteries.
    """
    if delete_all:
        logger.warning("Deleting all batteries")
        try:
            response = requests.delete(f"{API_BASE}/batteries", params={"all": True})
            if response.status_code == 200:
                logger.info("All batteries deleted successfully.")
            else:
                logger.error(f"Failed to delete all batteries: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            logger.exception(f"Error deleting all batteries: {str(e)}")
        return

    for battery_id in battery_ids:
        logger.info(f"Deleting battery {battery_id}")
        try:
            response = requests.delete(f"{API_BASE}/battery/{battery_id}")
            if response.status_code == 200:
                logger.info(f"Battery {battery_id} deleted successfully.")
            else:
                logger.error(f"Failed to delete battery {battery_id}: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            logger.exception(f"Error deleting battery {battery_id}: {str(e)}")
