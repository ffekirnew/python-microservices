import os
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

config: Dict[str, Dict[str, str]] = {
    "JWT": {
        "SECRET": os.getenv("SECRET"),
    },
    "MONGO": {
        "CONNECTION_STRING": os.getenv("CONNECTION_STRING"),
        "DB_NAME": os.getenv("DB_NAME"),
    },
    "AUTH_SERVICE_URL": os.getenv("AUTH_SERVICE_URL"),
}
