from contextvars import ContextVar

from webframework.types import Method, Path


class Request:
    method: Method
    path: Path
    path_params: dict

    def __init__(self, method: Method, path: Path, path_params: dict) -> None:
        self.method = method
        self.path = path
        self.path_params = path_params


request_var: ContextVar[Request] = ContextVar("request_var")
