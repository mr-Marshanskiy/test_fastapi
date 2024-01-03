from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.apps import app
from config.services import get_async_session, create_db_and_tables


@app.on_event('startup')
async def on_startup(session: AsyncSession = Depends(get_async_session)):
    await create_db_and_tables()
