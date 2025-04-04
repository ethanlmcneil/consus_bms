import requests
from app.core.logging import logger  # Centralized logger

API_BASE = "http://127.0.0.1:8000"  # Assumes your FastAPI is running locally

def create_identifier(post_code: str, capacity: float) -> str:
    """
    Generates a human-readable battery ID based on postcode prefix and capacity.
    
    Format: PREFIX-XXXX-CAPACITY
    Example: N1-000A-10

    - PREFIX: first part of postcode (e.g., N1)
    - XXXX: hex counter of how many batteries already exist with that prefix
    - CAPACITY: integer part of capacity in kWh
    """

    try:
        location_prefix = post_code.strip().split()[0].upper()
        logger.debug(f"Extracted location prefix: {location_prefix}")
    except IndexError:
        logger.error(f"Invalid postcode format: '{post_code}'")
        raise ValueError("Invalid postcode format")

    try:
        response = requests.get(
            f"{API_BASE}/battery",
            params={"location_prefix": location_prefix}
        )
        response.raise_for_status()
        existing_batteries = response.json()
        count = len(existing_batteries)
        logger.info(f"Found {count} existing batteries for prefix {location_prefix}")
    except requests.RequestException as e:
        logger.warning(f"Failed to query existing batteries for {location_prefix} ({e}), defaulting count to 0")
        count = 0

    hex_number = f"{count + 1:04X}"
    identifier = f"{location_prefix}-{hex_number}-{int(capacity)}"
    logger.info(f"Generated identifier: {identifier}")
    return identifier
