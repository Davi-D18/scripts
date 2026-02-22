from pydantic import BaseModel, EmailStr, field_validator

from car_api.core.messages import users


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError(users.USER_MIN_LENGTH)
        return v
