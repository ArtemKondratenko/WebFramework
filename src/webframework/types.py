from collections.abc import Callable

from typing import Literal, Any

type Method = Literal["GET", "POST", "DELETE", "PUT"]

type PathPattern = str

type Path = str

type Handler = Callable[..., Any]
