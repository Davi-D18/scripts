from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from car_api.core.messages.users import PASSWORD_MIN_LENGTH, USER_MIN_LENGTH


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def username_min_length(cls, username):
        if len(username) < 4:
            raise ValueError(USER_MIN_LENGTH)
        
        return username
        
    @field_validator('password')
    def password_min_length(cls, password):
        if len(password) < 8:
            raise ValueError(PASSWORD_MIN_LENGTH)
        
        return password


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator('username')
    def username_min_length(cls, username):
        if len(username) < 4:
            raise ValueError(USER_MIN_LENGTH)
        
    @field_validator('password')
    def password_min_length(cls, password):
        if len(password) < 8:
            raise ValueError(PASSWORD_MIN_LENGTH)


class UserPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]
