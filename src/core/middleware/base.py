import time

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from core.middleware.utils import check_request_url


class BaseMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope=scope, receive=receive)
        headers = request.headers
        request.state.start_time = time.time()
        ip: str | None
        if "x-forwarded-for" in headers.keys():
            ip = headers['x-forwarded-for']
        else:
            ip = request.client.host if request.client else None

        if ip and "," in ip:
            request.state.ip = ip.split(",")[0]
        else:
            request.state.ip = ip

        request.state.is_not_auth = await check_request_url(request.url.path)
        try:
            await self.app(scope, receive, send)
        except Exception:
            response = JSONResponse({"detail": "test"}, status_code=500)
            await response(scope, receive, send)
            pass
