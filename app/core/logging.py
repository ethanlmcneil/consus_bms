# app/core/logger.py

import logging

# Create a global logger
logger = logging.getLogger("consus")
logger.setLevel(logging.INFO)  # You can set DEBUG, WARNING, ERROR based on env

# Avoid adding handlers multiple times
if not logger.hasHandlers():
    handler = logging.StreamHandler()  # Could be FileHandler if saving to file
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
