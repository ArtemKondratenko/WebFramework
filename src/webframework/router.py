from __future__ import annotations

from itertools import zip_longest
from typing import TYPE_CHECKING, Callable

type HandlerDecorator = Callable[[Handler], Handler]

if TYPE_CHECKING:
    from webframework.types import Method, Path, Handler, PathPattern


class Router:
    _handlers: list[tuple[Method, PathPattern, Handler]]

    def __init__(self) -> None:
        self._handlers = []

    def register(
        self, method: Method, path_pattern: PathPattern, handler: Handler
    ) -> None:
        """Регистрирует обработчик запроса, по методу и пути"""
        self._handlers.append((method, path_pattern, handler))
        self._path_pattern = path_pattern

    def get_handler_and_pattern(
        self, method: Method, path: Path
    ) -> tuple[Handler, PathPattern]:
        for registered_method, path_pattern, handler in self._handlers:
            if registered_method == method and _compare(path_pattern, path):
                return handler, path_pattern
        raise LookupError("Обработчик не найден")

    def get(self, path_pattern: PathPattern) -> HandlerDecorator:
        """Возвращает функцию по методу GET и пути"""

        def decorator(handler: Handler) -> Handler:
            self.register("GET", path_pattern, handler)
            return handler

        return decorator

    def post(self, path_pattern: PathPattern) -> HandlerDecorator:
        """Возвращает функцию по методу POST и пути"""

        def decorator(handler: Handler) -> Handler:
            self.register("POST", path_pattern, handler)
            return handler

        return decorator

    def put(self, path_pattern: PathPattern) -> HandlerDecorator:
        """Возвращает функцию по методу PUT и пути"""

        def decorator(handler: Handler) -> Handler:
            self.register("PUT", path_pattern, handler)
            return handler

        return decorator

    def delete(self, path_pattern: PathPattern) -> HandlerDecorator:
        """Возвращает функцию по методу DELETE и пути"""

        def decorator(handler: Handler) -> Handler:
            self.register("DELETE", path_pattern, handler)
            return handler

        return decorator


def _compare(path_pattern: PathPattern, path: Path) -> bool:
    """Проверяет одинаковость путей"""
    if path_pattern is None:
        return False
    parse_pattern = path_pattern.split("/")
    parse_path = path.split("/")
    if len(parse_pattern) != len(parse_path):
        return False
    for path_1, path_2 in zip_longest(parse_pattern, parse_path):
        if path_1 == path_2:
            continue
        if path_1 != path_2 and not path_1.startswith("{"):
            return False
    return True


def extract_path_params(path_pattern: str, path: str) -> dict:
    params = {}
    pattern_parts = path_pattern.strip("/").split("/")
    path_parts = path.strip("/").split("/")
    for ppat, pval in zip(pattern_parts, path_parts):
        if ppat.startswith("{") and ppat.endswith("}"):
            key = ppat[1:-1]
            params[key] = pval
    return params
