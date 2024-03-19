import pika

from src.core.config import config
from src.persistence.db_client import DbClient

db_client = DbClient(config["MONGO"]["CONNECTION_STRING"], config["MONGO"]["DB_NAME"])
fs = db_client.get_fs()
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()
