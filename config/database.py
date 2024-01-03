from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


# TODO: move to .env
DATABASE_URL = 'sqlite+aiosqlite:///test.db'

engine = create_async_engine(DATABASE_URL)
Base = declarative_base()
async_session_maker = async_sessionmaker(engine)



