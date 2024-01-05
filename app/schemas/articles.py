from app.schemas.base import BaseSchema


class ArticleSchema(BaseSchema):
    id: int
    title: str
    text: str


class ArticleCreateSchema(BaseSchema):
    title: str
    text: str


class ArticleUpdateSchema(BaseSchema):
    title: str
    text: str
