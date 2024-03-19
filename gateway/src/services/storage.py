import json

import pika
from fastapi import UploadFile
from gridfs import GridFS
from pika.adapters.blocking_connection import BlockingChannel


def upload_file(
    file: UploadFile, fs: GridFS, channel: BlockingChannel, access: dict[str, str]
):
    # Upload file to storage
    try:
        file_id = fs.put(file)
    except Exception as e:
        raise e

    # Send message to queue
    message = {
        "video_fid": file_id,
        "converted_audio_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
    except Exception as e:
        fs.delete(file_id)
        raise e
