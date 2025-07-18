from ninja import Schema, ModelSchema
from .models import CustomUser, UserProfile
from typing import Optional
from pydantic import BaseModel

class ErrorSchema(Schema):
    message: str

class UserSchema(ModelSchema):
    class Config:
        model = CustomUser
        model_fields = ['id', 'phone_number', 'email', 'username', 'is_staff', 'user_type',]
        from_attributes = True

class RegisterSchema(Schema):
    username: str
    email: str
    phone_number: str
    password: str
    confirm_password: str 
    user_type: Optional[str] = 'job_seeker'



class LoginSchema(Schema):
    login_input: str
    password: str


class UserProfileSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    profile_picture: Optional[str]
    age: Optional[int]
    location: Optional[str]
    about: Optional[str]
    skills: Optional[str]
    cv: Optional[str]
    user: UserSchema

    class Config:
        from_attributes = True

class AuthTokenSchema(Schema):
    access_token: str
    refresh_token: str

class UserResponseSchema(Schema):
    user: UserSchema
    tokens: AuthTokenSchema


class UpdateUserSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None
    about: Optional[str] = None
    skills: Optional[str] = None
    cv: Optional[str] = None


class ChangePasswordSchema(Schema):
    old_password: str
    new_password: str
    confirm_password: str