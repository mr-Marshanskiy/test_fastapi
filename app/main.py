from fastapi import FastAPI
from sqlalchemy import create_engine

from app.backend.config import config
from app.const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
from app.models.base import SQLModel
from app.routers import (
    auth,
    articles,
)
from app.version import __version__


app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={'defaultModelsExpandDepth': -1},
)

SQLModel.metadata.create_all(
    create_engine(config.database.dsn)
)

app.include_router(auth.router)
app.include_router(articles.router)
