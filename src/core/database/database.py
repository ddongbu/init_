from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from typing import Dict

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)

from config import settings


class DatabaseSessionManager:
    session_context: ContextVar[str] = ContextVar("session_context")

    def __init__(self):
        self.engines = {
            "FLIP": create_async_engine(str(settings.FLIP_DB)),
            "RESUME": create_async_engine(str(settings.RESUME_DB)),
            "RECRUIT": create_async_engine(str(settings.RECRUIT_DB)),
            "SYSTEM": create_async_engine(str(settings.SYSTEM_DB)),
        }

        self._async_session_factory = {
            name:
                async_sessionmaker(
                    class_=AsyncSession,
                    bind=engine,
                    expire_on_commit=False,
                )
            for name, engine in self.engines.items()
        }

        self.session: Dict[str, async_scoped_session] = {
            name: async_scoped_session(
                session_factory=self._async_session_factory.get(name),
                scopefunc=self.get_session_context,
            )
            for name, engine in self.engines.items()
        }

    def get_session_context(self) -> str:
        return self.session_context.get()

    def set_session_context(self, session_id: str) -> Token:
        return self.session_context.set(session_id)

    def reset_session_context(self, context: Token) -> None:
        self.session_context.reset(context)

    @asynccontextmanager
    async def get_read_session(self, db):
        _session = async_sessionmaker(
            class_=AsyncSession,
            bind=self.engines.get(db),
            expire_on_commit=False,
        )()
        try:
            yield _session
        finally:
            await _session.close()

    async def fetch_first(self, db, query):
        session = self.session.get(db)
        async with session() as read_session:
            result = await read_session.scalars(query)
            return result.first()

    async def fetch_one(self, db, query):
        session: async_scoped_session = self.session.get(db)
        async with session() as read_session:
            result = await read_session.execute(query)
            return result.one_or_none()

    async def fetch_join_all(self, db, query):
        session: async_scoped_session = self.session.get(db)
        async with session() as read_session:
            result = await read_session.execute(query)
            return result.unique().all()

    async def fetch_all(self, db, query):
        session: async_scoped_session = self.session.get(db)
        async with session() as read_session:
            result = await read_session.execute(query)
            return result.scalars().all()


database = DatabaseSessionManager()
