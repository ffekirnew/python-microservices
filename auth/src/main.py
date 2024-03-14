import dataclasses
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

from src.config import config
from src.db_client import DbClient

app = FastAPI()
auth_db_client = DbClient().get_collection("auth")


@dataclasses.dataclass
class User:
    username: str
    password: str
    _id: str

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return dataclasses.asdict(self)


class AuthDto(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(loginDto: AuthDto):
    record = auth_db_client.find_one({"username": loginDto.username})
    if not record:
        return {"error": "Not Authorized."}

    user = User.from_dict(record)

    if user.password != loginDto.password:
        return {"error": "Not Authorized."}

    return {"token": create_jwt(user.username, True)}


@app.post("/register")
async def register(registerDto: AuthDto):
    new_user = User(registerDto.username, registerDto.password, "")
    new_user_id = auth_db_client.insert_one(new_user.to_dict())
    if new_user_id is not None:
        return {"success": True}

    return {"error": "Try again."}


@app.get("/")
async def test(request: Request, response: Response):
    header = request.headers.get("Authorization")

    return validate_jwt(header if header is not None else "")


def create_jwt(username: str, is_admin: bool) -> str:
    payload = {
        "username": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),
        "iat": datetime.now(tz=timezone.utc),
        "admin": is_admin,
    }

    return jwt.encode(payload, config["JWT"]["SECRET"])


def validate_jwt(token: str):
    return jwt.decode(token, config["JWT"]["SECRET"])
