import os
import logging
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "herokumngr.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


class Config(object):
    LOGGER = True

    TG_BOT_TOKEN = "5311406598:AAHAHyNvEMBYr-meScihJ7v3ScCa_fnIZIw"

    OWNER_ID = int("5007505106")

    # Get from my.telegram.org
    API_ID = int("12429107")

    # Get from my.telegram.org
    API_HASH = "2c1096dfd767dfdfab961bb2fffe6be3"

    DONATION_LINK = None
    WORKERS = 8


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
