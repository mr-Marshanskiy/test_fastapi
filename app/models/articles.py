import datetime

from sqlalchemy import (
    ForeignKey, String, Text, BigInteger, DateTime
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.const import DEFAULT_SCHEMA
from app.models.base import SQLModel


class ArticleModel(SQLModel):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text)

    author_id: Mapped[int] = mapped_column(
        "author_id", ForeignKey(f"{DEFAULT_SCHEMA}.users.id")
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
    )
