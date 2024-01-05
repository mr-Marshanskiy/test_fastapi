from enum import Enum
from typing import (
    Final,
    List,
)


# Open API parameters
OPEN_API_TITLE: Final = "Test task FastAPI"
OPEN_API_DESCRIPTION: Final = "Test task FastAPI"

# Authentication service constants
AUTH_TAGS: Final[List[str | Enum] | None] = ["Authentication"]
AUTH_URL: Final = "token"
AUTH_REG_URL: Final = "reg"

TOKEN_TYPE: Final = "bearer"
TOKEN_EXPIRE_MINUTES: Final = 60

# Algorithm used to sign the JWT tokens
TOKEN_ALGORITHM: Final = "HS256"

# Articles service constants
ARTICLES_TAGS: Final[List[str | Enum] | None] = ["Articles"]
ARTICLES_URL: Final = "articles"

# DB schemas
DEFAULT_SCHEMA: Final = "myapi"

# Group permissions
ADMIN_GROUP = "admin"
