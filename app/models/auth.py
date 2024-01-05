import datetime
from typing import List

from sqlalchemy import (
    ForeignKey, String, BigInteger, DateTime
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship,
)

from app.const import DEFAULT_SCHEMA
from app.models.base import SQLModel


class GroupModel(SQLModel):
    __tablename__ = "groups"

    code: Mapped[str] = mapped_column(String(31), primary_key=True)
    name: Mapped[str] = mapped_column(String(127))
    users: Mapped[List["GroupUserModel"]] = relationship("GroupUserModel")


class UserModel(SQLModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(127))
    password: Mapped[str] = mapped_column(String(255))

    groups: Mapped[List["GroupUserModel"]] = relationship("GroupUserModel")


class GroupUserModel(SQLModel):
    __tablename__ = "groups_users"

    group_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DEFAULT_SCHEMA}.groups.code"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DEFAULT_SCHEMA}.users.id"), primary_key=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now,
    )
