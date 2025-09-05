import inspect
from typing import Any
from webframework.types import Handler
from typing import Annotated, get_args, get_origin


class ProviderNotFoundError(Exception):
    pass


class Injector:
    _handler: Handler
    _args: list[Any]
    _kwargs: dict[str, Any]

    def __init__(self, handler: Handler) -> None:
        self._handler = handler
        self._args = []
        self._kwargs = {}

    async def _get_parameter(self, param: inspect.Parameter) -> Any:
        """Возвращает значение аргумента если параметр является Annotated"""
        args = get_args(param.annotation)
        function = args[1]
        sig = inspect.signature(function)
        values = []
        for provider_param in sig.parameters.values():
            if get_origin(provider_param.annotation) is Annotated:
                values.append(await self._get_parameter(provider_param))
            elif provider_param.default is not inspect.Parameter.empty:
                values.append(provider_param.default)
            else:
                raise ProviderNotFoundError(
                    f"Cannot resolve parameter '{provider_param.name}' for provider '{function.__name__}'"
                )
        if inspect.iscoroutinefunction(function):
            return await function(*values)
        return function(*values)

    async def run(self) -> Any:
        """Заполняет поля инжектора args, kwargs из функции (hendlera)"""
        sig = inspect.signature(self._handler)
        params = list(sig.parameters.values())

        for param in params:
            value = None
            if get_origin(param.annotation) is Annotated:
                value = await self._get_parameter(param)
            elif param.default is not inspect.Parameter.empty:
                value = param.default

            if param.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            ):
                self._args.append(value)
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                self._kwargs[param.name] = value

        if inspect.iscoroutinefunction(self._handler):
            return await self._handler(*self._args, **self._kwargs)
        return self._handler(*self._args, **self._kwargs)
