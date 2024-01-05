from datetime import (
    datetime,
    timedelta,
)

from fastapi import (
    Depends,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import (
    jwt,
    JWTError,
)
from passlib.context import CryptContext
from sqlalchemy import select

from app import const
from app.backend.config import config
from app.const import (
    AUTH_URL,
    TOKEN_ALGORITHM,
    TOKEN_EXPIRE_MINUTES,
    TOKEN_TYPE,
)
from app.exc import raise_with_log
from app.models.auth import UserModel, GroupModel, GroupUserModel
from app.schemas.auth import (
    CreateUserSchema,
    TokenSchema,
    UserSchema, AuthUserSchema,
)
from app.services.base import (
    BaseDataManager,
    BaseService,
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl=AUTH_URL, auto_error=False)


async def get_current_user(token: str = Depends(oauth2_schema)) -> UserSchema | None:
    """Decode token to obtain user information.

    Extracts user information from token and verifies expiration time.
    If token is valid then instance of :class:`~app.schemas.auth.UserSchema`
    is returned, otherwise exception is raised.

    Args:
        token:
            The token to verify.

    Returns:
        Decoded user dictionary.
    """

    if token is None:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    try:
        # decode token using secret token key provided by config
        payload = jwt.decode(token, config.token_key, algorithms=[TOKEN_ALGORITHM])

        # extract encoded information
        id: int = int(payload.get("id", 0))
        name: str = payload.get("name")
        email: str = payload.get("email")
        expires_at: str = payload.get("expires_at")
        if email is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

        if is_expired(expires_at):
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Token expired")

        return UserSchema(id=id, name=name, email=email)
    except JWTError:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    return None


def is_expired(expires_at: str) -> bool:
    """Return :obj:`True` if token has expired."""

    return datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") < datetime.utcnow()


class HashingMixin:
    """Hashing and verifying passwords."""

    @staticmethod
    def bcrypt(password: str) -> str:
        """Generate a bcrypt hashed password."""

        return pwd_context.hash(password)

    @staticmethod
    def verify(password: str, plain_password: str) -> bool:
        """Verify a password against a hash."""

        return pwd_context.verify(plain_password, password)


class AuthService(HashingMixin, BaseService):
    """Authentication service."""

    def get_user(self, email: str) -> UserSchema:
        model = AuthDataManager(self.session).get_user_model(email)
        return UserSchema(
            id=model.id,
            name=model.name,
            email=model.email,
        )

    def create_user(self, user: CreateUserSchema) -> UserModel:
        """Add user with hashed password to database."""

        model_by_email = AuthDataManager(self.session).get_user_model(user.email)
        if isinstance(model_by_email, UserModel):
            raise_with_log(
                status.HTTP_400_BAD_REQUEST,
                "The user with specified email address already exists"
            )
        user_model = UserModel(
            name=user.name,
            email=user.email,
            password=self.bcrypt(user.password),
        )

        AuthDataManager(self.session).add_user(user_model)
        return user_model

    def authenticate(
        self, login: OAuth2PasswordRequestForm = Depends()
    ) -> TokenSchema | None:
        """Generate token.

        Obtains username and password and verifies password against
        hashed password stored in database. If valid then temporary
        token is generated, otherwise the corresponding exception is raised.
        """

        user = AuthDataManager(self.session).get_user(login.username)

        if user.password is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
        else:
            if not self.verify(user.password, login.password):
                raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
            else:
                access_token = self._create_access_token(user.id, user.name, user.email)
                return TokenSchema(access_token=access_token, token_type=TOKEN_TYPE)
        return None

    def is_admin(self, user: UserSchema):
        return AuthDataManager(self.session).is_admin(user.id)

    def _create_access_token(self, id: int, name: str, email: str) -> str:
        """Encode user information and expiration time."""

        payload = {
            "id": id,
            "name": name,
            "email": email,
            "expires_at": self._expiration_time(),
        }

        return jwt.encode(payload, config.token_key, algorithm=TOKEN_ALGORITHM)

    @staticmethod
    def _expiration_time() -> str:
        """Get token expiration time."""

        expires_at = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")


class AuthDataManager(BaseDataManager):
    def add_user(self, user: UserModel) -> None:
        """Write user to database."""

        self.add_one(user)

    def get_user(self, email: str) -> AuthUserSchema:
        """Read user from database."""

        model = self.get_user_model(email)

        return AuthUserSchema(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
        )

    def get_user_model(self, email: str) -> UserModel | None:
        return self.get_one(select(UserModel).where(UserModel.email == email))

    def is_admin(self, user_id) -> bool:
        model = self.get_one(select(GroupUserModel).where(
            GroupUserModel.user_id == user_id,
            GroupUserModel.group_id == const.ADMIN_GROUP
        ))
        return isinstance(model, GroupUserModel)


class GroupService(BaseService):
    """Group permissions service."""

    def get_or_create_admin_group(self) -> GroupModel:
        model = GroupDataManager(self.session).get_group_model(const.ADMIN_GROUP)

        if not isinstance(model, GroupModel):
            model = GroupModel(code=const.ADMIN_GROUP, name="Admin")
            GroupDataManager(self.session).add_one(model)
            return model
        return model

    def add_user_to_admin_group(self, user: UserModel) -> None:
        group = self.get_or_create_admin_group()
        group_user_model = GroupUserModel(user_id=user.id, group_id=group.code)
        GroupDataManager(self.session).add_one(group_user_model)
        return


class GroupDataManager(BaseDataManager):
    def get_group_model(self, code: str) -> GroupModel | None:
        return self.get_one(select(GroupModel).where(GroupModel.code == code))
