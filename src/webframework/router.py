from __future__ import annotations

from itertools import zip_longest
from typing import TYPE_CHECKING


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

    def get_handler(self, method: Method, path: Path) -> Handler:
        """Возвращает обрабтчик запроса, по методу и пути"""
        for registered_method, path_pattern, handler in self._handlers:
            if registered_method == method and _compare(path_pattern, path):
                return handler
        raise LookupError("Обработчик не найден")


def _compare(path_pattern: PathPattern, path: Path) -> bool:
    """Проверяет одинаковость путей"""
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
