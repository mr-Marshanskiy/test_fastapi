from pydantic import BaseModel


class UserListSerializer(BaseModel):
    id: int
    username: str
    email: str
