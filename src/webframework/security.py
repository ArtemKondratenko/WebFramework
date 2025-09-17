from __future__ import annotations

import base64

# base64.b64decode
# "login:password"

# Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==


class BasicHTTPAuthCredentials:
    login: str
    password: str

    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password

    @staticmethod
    def parse(raw: str) -> BasicHTTPAuthCredentials:
        line_encode = raw.replace("Basic", "").strip()
        decoded_bytes = base64.b64decode(line_encode.encode("utf-8"))
        login_password = decoded_bytes.decode("UTF-8")
        login, password = login_password.strip().split(":")
        return BasicHTTPAuthCredentials(login, password)
