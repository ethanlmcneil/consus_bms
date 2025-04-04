from cems.scripts.battery_monitoring.fetch_batteriesDB import fetch_all_batteries
from app.core.logging import logger
import time

from scripts.control.action_logic import ActionController
def action_logic_loop(interval: int = 20, max_failures: int = 5):
    logger.info("Starting battery monitor loop at interval of %d seconds", interval)

    failure_count = 0

    try:
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logger.debug(f"Polling batteries at {timestamp}")

            try:
                batteries = fetch_all_batteries()
            except Exception as fetch_error:
                failure_count += 1
                logger.warning(f"Failed to fetch battery data (attempt {failure_count}/{max_failures}): {fetch_error}")
                if failure_count >= max_failures:
                    logger.error("Max API failure limit reached. Terminating monitor loop.")
                    break
                time.sleep(interval)
                continue

            if not batteries:
                failure_count += 1
                logger.warning(f"No batteries returned (attempt {failure_count}/{max_failures})")
                if failure_count >= max_failures:
                    logger.error("Max empty response limit reached. Terminating monitor loop.")
                    break
                time.sleep(interval)
                continue
            else:
                failure_count = 0  # Reset on success

            for battery in batteries:
                try:
                    controller = ActionController(battery)
                    action = controller.decide()
                    logger.info(f"Battery {battery['identifier']} action: {action} at {timestamp}")
                except Exception as battery_error:
                    logger.exception(f"Error processing battery {battery.get('identifier', 'UNKNOWN')}: {battery_error}")

            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Battery monitor loop terminated by user.")

    except Exception as e:
        logger.exception(f"Unexpected error in battery monitor loop: {e}")
