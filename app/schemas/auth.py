from app.schemas.base import BaseSchema


class CreateUserSchema(BaseSchema):
    name: str
    email: str
    password: str


class UserSchema(BaseSchema):
    id: int
    name: str
    email: str


class AuthUserSchema(BaseSchema):
    id: int
    name: str
    email: str
    password: str


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str


class CreateGroupSchema(BaseSchema):
    code: str
    name: str


class CreateGroupUserSchema(BaseSchema):
    user_id: int
    group_id: int
