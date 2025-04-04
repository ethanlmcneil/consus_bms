import requests
import time
from typing import List, Dict
from cems.global_var import API_BASE


#API_BASE = "http://127.0.0.1:8000"

from app.core.logging import logger

def fetch_all_batteries() -> List[Dict]:
    try:
        response = requests.get(f"{API_BASE}/batteries", timeout=5)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data
        else:
            logger.warning("Unexpected response format from /batteries")
            return []

    except requests.RequestException as e:
        logger.error(f"Failed to fetch batteries: {e}")
        return []

