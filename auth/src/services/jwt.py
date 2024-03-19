from datetime import datetime, timedelta, timezone

import jwt

from src.core.config import config


def create_jwt(username: str, is_admin: bool) -> str:
    payload = {
        "username": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),
        "iat": datetime.now(tz=timezone.utc),
        "admin": is_admin,
    }

    return jwt.encode(payload, config["JWT"]["SECRET"], algorithm="HS256")


def validate_jwt(token: str):
    return jwt.decode(token, config["JWT"]["SECRET"], algorithms=["HS256"])
