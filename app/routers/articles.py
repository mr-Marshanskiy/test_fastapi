from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.backend.session import create_session
from app.const import (
    ARTICLES_TAGS,
    ARTICLES_URL,
)
from app.schemas.auth import UserSchema
from app.schemas.articles import ArticleSchema, ArticleCreateSchema, \
    ArticleUpdateSchema
from app.services.auth import get_current_user
from app.services.articles import ArticleService


router = APIRouter(prefix="/" + ARTICLES_URL, tags=ARTICLES_TAGS)


@router.get("/", response_model=List[ArticleSchema])
async def get_articles(
    session: Session = Depends(create_session),
) -> List[ArticleSchema]:
    """Get articles."""

    return ArticleService(session).get_articles()


@router.get("/{id}", response_model=ArticleSchema)
async def get_article(
    id: int,
    session: Session = Depends(create_session),
) -> ArticleSchema:
    """Get article by id."""

    return ArticleService(session).get_article(id)


@router.post("/", response_model=ArticleSchema)
async def post_article(
    item: ArticleCreateSchema,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> ArticleSchema:
    """Create article."""

    model = ArticleService(session).create_article(item, user.id)
    return ArticleService(session).get_article(model.id)


@router.put("/{id}", response_model=ArticleSchema)
async def update_article(
    id: int,
    item: ArticleUpdateSchema,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> ArticleSchema:
    """Update article."""

    model = ArticleService(session).get_article_model(id)
    ArticleService(session).check_obj_exists_or_raise(model)
    ArticleService(session).check_has_permissions_to_edit(model, user)
    ArticleService(session).update_article(model, item)
    return ArticleService(session).get_article(model.id)
