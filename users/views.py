import typing

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.apps import app
from users.models import User
from users.serializers import UserListSerializer
from config.services import get_async_session


@app.get('/users/', tags=['Users'])
async def get_users(session: AsyncSession = Depends(get_async_session)) -> typing.List[UserListSerializer]:
    users = await session.execute(select(User))
    return [UserListSerializer(
        id=user.id,
        username=user.username,
        email=user.email,
    ) for user in users.scalars()]


@app.get('/users/{id}/', tags=['Users'])
async def get_users_detail(session: AsyncSession = Depends(get_async_session)) -> UserListSerializer:
    user = await session.get(User, id)
    if user:
        return UserListSerializer(
            id=user.id,
            username=user.username,
            email=user.email,
        )
