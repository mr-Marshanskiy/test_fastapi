import typing

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from articles.models import Article
from articles.serializers import ArticleListSerializer, ArticleCreateSerializer
from config.apps import app
from config.services import get_async_session


@app.get('/articles/', tags=['Articles'])
async def get_articles(session: AsyncSession = Depends(get_async_session)) -> typing.List[ArticleListSerializer]:
    articles = await session.execute(select(Article))
    return [ArticleListSerializer(
        id=article.id,
        title=article.title,
        text=article.text,
    ) for article in articles.scalars()]


@app.get('/articles/{id}/', tags=['Articles'])
async def get_articles_detail(id: int, session: AsyncSession = Depends(get_async_session)) -> ArticleListSerializer:
    article = await session.get(Article, id)
    if article:
        return ArticleListSerializer(
            id=article.id,
            title=article.title,
            text=article.text,
        )


@app.post('/articles/', tags=['Articles'])
async def post_articles(data: ArticleCreateSerializer, session: AsyncSession = Depends(get_async_session)):
    session.add(Article(title=data.title, text=data.text))
    await session.commit()
