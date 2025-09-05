import asyncio
from typing import Annotated


from webframework.injector import Injector


def test_get_parameter_str_argument_args() -> None:
    def f() -> str:
        return "Hello"

    def result(param: Annotated[str, f]) -> str:
        return param + " Artem"

    injector = Injector(result)

    assert asyncio.run(injector.run()) == "Hello Artem"


def test_get_parameter_int_argument_args() -> None:
    def f() -> int:
        return 2

    def result(param: Annotated[int, f]) -> int:
        return param * 5

    injector = Injector(result)

    assert asyncio.run(injector.run()) == 10


def test_get_parameter_str_argument_kwargs() -> None:
    def a() -> str:
        return "Hello "

    def f() -> str:
        return a() + "Artem"

    def result(param: Annotated[str, f]) -> str:
        return param + "!"

    injector = Injector(result)

    assert asyncio.run(injector.run()) == "Hello Artem!"


def test_default_parameter() -> None:
    def f() -> str:
        return "Artem"

    def result(param: Annotated[str, f], a="Hello ") -> str:
        return a + param + "!"

    injector = Injector(result)

    assert asyncio.run(injector.run()) == "Hello Artem!"


def test_0():
    async def get_a():
        return 1

    injector = Injector(get_a)

    assert asyncio.run(injector.run()) == 1


def test_1():
    async def get_a():
        return 1

    async def get_b(a: Annotated[int, get_a]):
        return a * 2

    async def get_c(a: Annotated[int, get_a], b: Annotated[int, get_b]):
        return a + b

    injector = Injector(get_c)
    assert asyncio.run(injector.run()) == 3


def test_2():
    async def get_a():
        return 1

    def get_b(a: Annotated[int, get_a]):
        return a * 2

    async def get_c(a: Annotated[int, get_a], b: Annotated[int, get_b]):
        return a + b

    async def get_d(c: Annotated[int, get_c]):
        return c + 1

    injector = Injector(get_d)
    assert asyncio.run(injector.run()) == 4


def test_3():
    def get_a():
        return 1

    async def get_b(*, a: Annotated[int, get_a]):
        return a * 2

    injector = Injector(get_b)

    assert asyncio.run(injector.run()) == 2
