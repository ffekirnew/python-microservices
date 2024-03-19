from typing import Annotated

from fastapi import Depends, FastAPI, UploadFile
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from src.infrastructure.queue import channel, fs
from src.services import auth
from src.services.storage import upload_file

app = FastAPI()
basic_auth = HTTPBasic()
bearer_auth = HTTPBearer()


@app.get("/login")
def login(credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)]):
    try:
        response = auth.login(credentials.username, credentials.password)
    except Exception:
        return {"message": "Invalid credentials"}
    return {"token": response["token"]}


@app.post("/upload")
def upload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth)],
    file: UploadFile,
):
    token = credentials.credentials
    try:
        access = auth.authenticate(token)
    except Exception:
        return {"message": "Unauthorized"}

    if file is None:
        return {"message": "Invalid number of files"}

    print(file)
    if file.content_type != "video/mp4":
        return {"message": "Invalid file type"}

    print(access, file.filename)

    try:
        upload_file(file, fs, channel, access)
    except Exception:
        return {"message": "File upload failed"}

    return {"message": "File uploaded"}
