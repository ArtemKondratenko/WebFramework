from contextvars import ContextVar

from webframework.types import Method, Path
from collections.abc import Callable


class Request:
    method: Method
    path: Path
    path_params: dict

    def __init__(self, method: Method, path: Path, path_params: dict) -> None:
        self.method = method
        self.path = path
        self.path_params = path_params


request_var: ContextVar[Request] = ContextVar("request_var")


def path(name: str) -> Callable[[], str]:
    def wrapper():
        return request_var.get().path_params[name]

    return wrapper


def parsed(function: Callable, parser: type) -> Callable:
    def wrapper():
        return parser(function())

    return wrapper
