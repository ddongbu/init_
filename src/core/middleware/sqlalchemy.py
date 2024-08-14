from uuid import uuid4

from starlette.types import ASGIApp, Receive, Scope, Send

from core.database.database import database


class SQLAlchemyMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):

        # DB 세션이 필요 없는 경로
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        session_id = str(uuid4())
        context = database.set_session_context(session_id=session_id)
        await self.app(scope, receive, send)

        await database.session.get('SYSTEM').remove()
        database.reset_session_context(context=context)
