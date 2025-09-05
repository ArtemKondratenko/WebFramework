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
        handler, path_pattern = self._router.get_handler_and_pattern(method, path)
        path_params = extract_path_params(path_pattern, path)
        request = Request(method, path, path_params)
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
