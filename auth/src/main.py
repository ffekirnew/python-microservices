from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.dtos.auth_dto import AuthDto
from src.entities.user import User
from src.persistence.db_client import DbClient
from src.services.jwt import create_jwt, validate_jwt

app = FastAPI()
security = HTTPBearer()
auth_db_client = DbClient().get_collection("auth")


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


@app.post("/authenticate")
async def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    return validate_jwt(token)
