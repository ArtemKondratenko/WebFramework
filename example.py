from __future__ import annotations

import json
from typing import Annotated, Any

import uvicorn

from webframework.application import App
from webframework.request import body, parsed, path
from webframework.response import Response
from webframework.router import Router


class User:
    admin: bool
    login: str
    password: str

    def __init__(self, admin: bool, login: str, password: str) -> None:
        self.admin = admin
        self.login = login
        self.password = password

    @staticmethod
    def from_dict(obj: dict[str, Any]) -> User:
        return User(**obj)


db = dict[str, User]()
router = Router()


@router.post("/users")
async def create_user(
    user: Annotated[User, parsed(body(), User.from_dict)],
) -> Response:
    db[user.login] = user
    data = {"admin": user.admin, "login": user.login}
    return Response(
        201, json.dumps(data).encode(), {"Content-Type": "application/json"}
    )


@router.delete("/users/{user_login}")
async def delete_user(
    user_login: Annotated[str, parsed(path("user_login"), str)],
) -> Response:
    """
    Удаляет пользователя по логину.
    - 404, если пользователь не найден.
    - 403, если пользователь не является администратором (удалять нельзя).
    - 204 No Content при успешном удалении.
    """
    user = db.get(user_login)
    if user is None:
        return Response(
            404,
            json.dumps({"detail": "User not found"}).encode(),
            {"Content-Type": "application/json"},
        )

    if not user.admin:
        return Response(
            403,
            json.dumps({"detail": "Cannot delete admin user"}).encode(),
            {"Content-Type": "application/json"},
        )

    del db[user_login]
    return Response(204, b"", {})


@router.get("/user/{user_login}")
async def get_info_user(
    user_login: Annotated[str, parsed(path("user_login"), str)],
) -> Response:
    """
    Предоставляет инфу о пользователе по логину
    - 404, если пользователь не найден.
    - 201 при успешной отправке информации о пользователе.
    """
    user = db.get(user_login)
    if user is None:
        return Response(
            404,
            json.dumps({"detail": "User not found"}).encode(),
            {"Content-Type": "application/json"},
        )

    data = {"admin": user.admin, "login": user.login}
    return Response(
        201, json.dumps(data).encode(), {"Content-Type": "application/json"}
    )


@router.put("/users/{admin_login}")
async def put_info_user(
    admin_login: Annotated[str, parsed(path("admin_login"), str)],
    maybe_user_to_delete: Annotated[User, parsed(body(), User.from_dict)],
) -> Response:
    """
    Удаляет пользователя по логину.
    - 404, если админ или пользователь не найден.
    - 403, если пользователь-админ  не является администратором (удалять нельзя).
    - 204 No Content при успешном изменнии инфы.
    """
    admin = db.get(admin_login)
    user_to_delete = db.get(maybe_user_to_delete.login)
    if admin is None or user_to_delete is None:
        return Response(
            404,
            json.dumps({"detail": "Admin or user not found"}).encode(),
            {"Content-Type": "application/json"},
        )

    if not admin.admin:
        return Response(
            403,
            json.dumps({"detail": "User is not admin"}).encode(),
            {"Content-Type": "application/json"},
        )

    db[user_to_delete.login] = user_to_delete
    return Response(204, b"", {})


app = App(router)

uvicorn.run(app)
