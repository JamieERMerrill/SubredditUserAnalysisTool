# Copyright (c) 2018 by James Merrill, all rights reserved

import logging


def configure_logging():
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging startup.")