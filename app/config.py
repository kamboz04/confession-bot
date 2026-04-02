#only read env file

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_CONFIG = {
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
    "dbname": os.getenv("PG_DB"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
}

TIMEZONE = os.getenv("APP_TIMEZONE", "UTC")
