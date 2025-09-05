from collections.abc import Callable, Awaitable

from typing import Literal, Any


type Method = Literal["GET", "POST", "DELETE", "PUT"]

type PathPattern = str

type Path = str

type Handler = Callable[..., Any]

type Message = dict[str, Any]

type Scope = Message

type Receive = Callable[[], Awaitable[Message]]

type Send = Callable[[Message], Awaitable[None]]
