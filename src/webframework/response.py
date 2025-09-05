# status: int, body: bytes, headers: dict[str, str]

# dict[str, str] → list[tuple[bytes, bytes]]


class Response:
    status: int
    body: bytes
    headers: dict[str, str]

    def __init__(self, status: int, body: bytes, headers: dict):
        self.status = status
        self.body = body
        self.headers = headers


def convert_dict_to_list(headers: dict) -> list[tuple[bytes, bytes]]:
    return [(k.encode(), v.encode()) for k, v in headers.items()]
