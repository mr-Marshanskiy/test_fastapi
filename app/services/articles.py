from typing import List

from fastapi import (
    status,
)

from sqlalchemy import select

from app.exc import raise_with_log
from app.models.articles import ArticleModel
from app.schemas.articles import ArticleSchema, ArticleCreateSchema, \
    ArticleUpdateSchema
from app.schemas.auth import UserSchema
from app.services.auth import AuthService
from app.services.base import (
    BaseDataManager,
    BaseService,
)


class ArticleService(BaseService):
    def get_article(self, article_id: int) -> ArticleSchema:
        return ArticleDataManager(self.session).get_article(article_id)

    def get_article_model(self, article_id: int) -> ArticleModel:
        return ArticleDataManager(self.session).get_article_model(article_id)

    def get_articles(self) -> List[ArticleSchema]:
        return ArticleDataManager(self.session).get_articles()

    def create_article(
            self,
            item: ArticleCreateSchema,
            author_id: int,
    ) -> ArticleModel:

        model = ArticleModel(
            title=item.title,
            text=item.text,
            author_id=author_id,
        )
        ArticleDataManager(self.session).add_one(model)
        return model

    def update_article(self, model: ArticleModel, item: ArticleUpdateSchema):
        ArticleDataManager(self.session).update_one(model, item)

    def check_obj_exists_or_raise(
            self,
            model: ArticleModel,
            status_code: int = status.HTTP_404_NOT_FOUND,
            message: str = "Not found."
    ):
        if not isinstance(model, ArticleModel):
            raise_with_log(status_code, message)

    def check_has_permissions_to_edit(
            self,
            model: ArticleModel,
            user: UserSchema,
    ):
        if model.created_at == user.id:
            return True
        if AuthService(self.session).is_admin(user):
            return True
        raise raise_with_log(
            status.HTTP_400_BAD_REQUEST,
            "You don't have permissions to edit this article."
        )


class ArticleDataManager(BaseDataManager):
    def get_article_model(self, article_id: int) -> ArticleModel:
        stmt = select(ArticleModel).where(ArticleModel.id == article_id)
        model = self.get_one(stmt)
        return model

    def get_article(self, article_id: int) -> ArticleSchema:
        model = self.get_article_model(article_id)
        if not isinstance(model, ArticleModel):
            raise_with_log(status.HTTP_404_NOT_FOUND, "Article not found.")

        return ArticleSchema(**model.to_dict())

    def get_articles(self) -> List[ArticleSchema]:
        schemas: List[ArticleSchema] = list()

        stmt = select(ArticleModel)

        for model in self.get_all(stmt):
            schemas += [ArticleSchema(**model.to_dict())]

        return schemas
