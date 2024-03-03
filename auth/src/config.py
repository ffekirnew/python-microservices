import os

from dotenv import load_dotenv

load_dotenv()

config = {
    "JWT": {
        "SECRET": os.getenv("SECRET"),
    },
    "MONGO": {
        "CONNECTION_STRING": os.getenv("CONNECTION_STRING"),
        "DB_NAME": os.getenv("DB_NAME"),
    },
}
