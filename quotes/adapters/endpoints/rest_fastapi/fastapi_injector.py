"""
A simple integration of alecthomas' injector into FastAPI.
Exposes a dependency wrapper to use in your routes.
"""

from typing import Any, TypeVar
import jwt
from fastapi import Depends, FastAPI, Request
from injector import Injector

class EUserNotFoundOnToken(Exception):
    pass


class InjectorNotAttached(ValueError):
    """Raised when Injected is used without an injector instance attached to the app."""


def attach_injector(app: FastAPI, injector: Injector) -> None:
    """Call this function on app startup to attach an injector to the app."""
    app.state.injector = injector


def get_injector_instance(app: FastAPI) -> Injector:
    """
    Returns the injector instance attached to the app.
    """
    try:
        return app.state.injector
    except AttributeError as exc:
        raise InjectorNotAttached(
            "No injector instance has been attached to the app."
        ) from exc


BoundInterface = TypeVar("BoundInterface", bound=type)


def Injected(interface: BoundInterface) -> Any:  # pylint: disable=invalid-name
    """
    Asks your injector instance for the specified type,
    allowing you to use it in the route.
    """

    def inject_into_route(request: Request) -> BoundInterface:
        return get_injector_instance(request.app).get(interface)

    return Depends(inject_into_route)


def get_userid_from_token(req: Request):
    requesContext = req.get("requestContext")

    token = req.headers.get("Authorization") 
    if token and ("Bearer" in token):
        _, token = token.split(" ")
        token_decoded = jwt.decode(token, options={"verify_signature": False})
        return token_decoded['username']

    raise EUserNotFoundOnToken()

__all__ = [
    "attach_injector",
    "get_injector_instance",
    "Injected",
    "InjectorNotAttached",
    'get_userid_from_token'
]