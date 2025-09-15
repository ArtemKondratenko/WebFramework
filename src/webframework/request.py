from contextvars import ContextVar
import json
from typing import Any

from webframework.types import Method, Path
from collections.abc import Callable


class Request:
    method: Method
    path: Path
    path_params: dict
    body: dict
    headers: dict

    def __init__(
        self, method: Method, path: Path, path_params: dict, body: bytes, headers: dict
    ) -> None:
        self.method = method
        self.path = path
        self.path_params = path_params
        decoded = body.decode("utf-8").strip()
        self.body = json.loads(decoded) if decoded else {}
        self.headers = headers


request_var: ContextVar[Request] = ContextVar("request_var")


def path(name: str) -> Callable[[], str]:
    def wrapper():
        return request_var.get().path_params[name]

    return wrapper


def body(name: str | None = None) -> Callable[[], Any]:
    def wrapper():
        if name is not None:
            return request_var.get().body[name]
        return request_var.get().body

    return wrapper


def header(name: str) -> Callable[[], Any]:
    def wrapper():
        return request_var.get().headers.get(name.lower())

    return wrapper


def parsed(function: Callable, parser: Any) -> Callable:
    def wrapper():
        result = parser(function())
        return result

    return wrapper
