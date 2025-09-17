import pytest
from webframework.router import Router, _compare


def test_compare_paths() -> None:
    paths = [
        ("/users/{id}/friends", "/users/vanya/friends"),
        ("/", "/"),
        ("/{a}/b/{c}", "/a/b/c"),
    ]
    assert all(_compare(path_pattern, path) for path_pattern, path in paths)

    paths = [
        ("/users/{id}", "/users/vanya/friends"),
        ("/", ""),
        ("/g/b/{c}", "/a/b/c"),
    ]
    assert not all(_compare(path_pattern, path) for path_pattern, path in paths)


def test_register() -> None:
    router = Router()

    def f():
        pass

    method = "GET"
    path = "/users/vanya/friends"
    handler = f

    router.register(method, path, handler)

    assert len(router._handlers) == 1

    router.register(method, path, handler)

    assert len(router._handlers) == 2


def test_get_handler_is_there() -> None:
    router = Router()

    def f():
        pass

    method = "GET"
    path = "/users/vanya/friends"
    handler = f
    router.register(method, path, handler)

    assert router.get_handler_and_pattern(method, path) is f


def test_get__no_handler() -> None:
    router = Router()

    def f():
        pass

    method = "GET"
    path = "/users/vanya/friends"
    handler = f
    router.register(method, path, handler)

    with pytest.raises(LookupError):
        router.get_handler_and_pattern(method="POST", path="/users/vanya/friends")
