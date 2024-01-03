import typing

from pydantic import BaseModel


class ArticleListSerializer(BaseModel):
    id: int
    title: str
    text: str


class ArticleCreateSerializer(BaseModel):
    title: str
    text: str


class ArticleUpdateSerializer(BaseModel):
    title: typing.Optional[str]
    text: typing.Optional[str]
