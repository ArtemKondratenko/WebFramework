from webframework.request import Request
from webframework.types import Scope, Receive, Send
from webframework.router import Router, extract_path_params
from webframework.injector import Injector
from webframework.response import convert_dict_to_list, Response
from webframework.request import request_var


class App:
    _router: Router

    def __init__(self, router: Router) -> None:
        self._router = router

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        method = scope["method"]
        path = scope["path"]
        headers = scope_headers_in_dict(scope)
        handler, path_pattern = self._router.get_handler_and_pattern(method, path)
        path_params = extract_path_params(path_pattern, path)
        body = await _get_body(receive)
        request = Request(method, path, path_params, body, headers)
        request_var.set(request)
        response: Response = await Injector(handler).run()
        await send(
            {
                "type": "http.response.start",
                "status": response.status,
                "headers": convert_dict_to_list(response.headers),
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": response.body,
            }
        )


async def _get_body(receive: Receive) -> bytes:
    body = bytes()
    while True:
        result = await receive()
        more_body = result.get("more_body")
        body += result["body"]
        if not more_body:
            break
    return body


def scope_headers_in_dict(scope: Scope) -> dict[str, str]:
    result = {}
    headers = scope["headers"]
    for k, v in headers:
        result[k.decode().lower()] = v.decode()
    return result
