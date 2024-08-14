import secrets

from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send


class CSRFMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        request = Request(scope=scope, receive=receive)
        csrf_token_cookie = request.cookies.get('csrf_token')

        if request.state.is_not_auth:
            return await self.app(scope, receive, send)

        if request.method in ("POST", "PUT", "DELETE"):
            csrf_token_header = request.headers.get('x-csrf-token')
            if not csrf_token_cookie or csrf_token_header != csrf_token_cookie:
                # 토큰에러
                raise Exception
        response = Response()
        csrf_token = secrets.token_urlsafe(16)
        response.set_cookie(key="csrf-token", value=csrf_token, httponly=True, samesite='strict')
        response.headers["x-csrf-token"] = csrf_token
        await response(scope, receive, send)

        await self.app(scope, receive, send)
