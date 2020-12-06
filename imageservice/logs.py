import logging
from os import environ

def init():
    loglevel = environ.get("LOGLEVEL", "WARNING")
    numeric_level = getattr(logging, loglevel, logging.WARNING)
    logging.basicConfig(level=numeric_level, format='%(asctime)s %(message)s')