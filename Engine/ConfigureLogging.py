import logging


def configure_logging():
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging startup.")