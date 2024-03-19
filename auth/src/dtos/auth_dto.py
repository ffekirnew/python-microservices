from pydantic import BaseModel


class AuthDto(BaseModel):
    username: str
    password: str
