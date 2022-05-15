from app.store import get_store

from .users import InternalException, IUsersApp, UserApp  # noqa: F401


def get_domain_app() -> IUsersApp:
    return UserApp(get_store())
