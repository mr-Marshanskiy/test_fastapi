import click

from app.backend.session import open_session
from app.schemas.auth import CreateUserSchema
from app.services.auth import AuthService, GroupService
from app.version import __version__


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show package version")
def main(version: bool) -> None:
    """Welcome to API command line!"""

    if version:
        click.echo("Version: " + __version__)


@main.command()
@click.option("--name", type=str, help="User name")
@click.option("--email", type=str, help="Email")
@click.option("--password", type=str, help="Password")
def create_user(name: str, email: str, password: str) -> None:
    """Create new user.

    Write new user (with hashed password) to corresponding database table.

    \b
    Examples:
        myapi create-user --name 'test user' --email test_user@myapi.com --password qwerty
    """

    # initialize user schema
    user = CreateUserSchema(name=name, email=email, password=password)

    # write to database
    with open_session() as session:
        AuthService(session).create_user(user)


@main.command()
@click.option("--name", type=str, help="User name")
@click.option("--email", type=str, help="Email")
@click.option("--password", type=str, help="Password")
def create_admin_user(name: str, email: str, password: str) -> None:
    """Create new admin user.

    Write new user (with hashed password) to corresponding database table.

    \b
    Examples:
        myapi create-admin-user --name 'test user' --email test_user@myapi.com --password qwerty
    """

    # initialize schema
    user = CreateUserSchema(name=name, email=email, password=password)

    # write to database
    with open_session() as session:
        user_model = AuthService(session).create_user(user)
        GroupService(session).add_user_to_admin_group(user_model)
