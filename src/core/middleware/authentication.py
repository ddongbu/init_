from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send


class Authentication:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope=scope, receive=receive)
        headers = request.headers
        url = request.url.path
        if request.state.is_not_auth:
            return await self.app(scope, receive, send)

        if url.startswith("/api"):
            if "authorization" in headers.keys() and "refresh-token" in request.cookies.keys():
                # 토큰확인
                pass

                await self.app(scope, receive, send)
            else:
                # 에러처리
                raise Exception
