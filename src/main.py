from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import APIRouter, FastAPI
from redis import Redis
from redis.asyncio import ConnectionPool
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from config import app_configs, settings
from core.authentication.oauth2 import VdreamOAuth
from core.authentication.token import VdreamToken
from core.database import redis
from core.logger import init_logger
from core.middleware.authentication import Authentication
from core.middleware.base import BaseMiddleware
from core.middleware.csrf import CSRFMiddleware
from core.middleware.sqlalchemy import SQLAlchemyMiddleware
from user.router import router as user_router
from core.websocket.router import router as websocket_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    redis_pool_t = ConnectionPool.from_url(
        str(settings.REDIS_URL_T),
        decode_responses=True,
        max_connections=100,
    )
    redis_pool_c = ConnectionPool.from_url(
        str(settings.REDIS_URL_T),
        decode_responses=True,
        max_connections=100,
    )
    redis.redis_token = Redis(connection_pool=redis_pool_t)
    redis.redis_code = Redis(connection_pool=redis_pool_c)
    yield
    await redis_pool_c.disconnect()
    await redis_pool_t.disconnect()


app = FastAPI(
    **app_configs, lifespan=lifespan
)

# Oauth 기능
oauth2 = VdreamOAuth(**settings.__dict__)

# Token 정의
token = VdreamToken(**settings.__dict__)

# Logger 정의
init_logger()

app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)
app.add_middleware(SQLAlchemyMiddleware)
app.add_middleware(CSRFMiddleware)
app.add_middleware(Authentication)
app.add_middleware(BaseMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter()
api.include_router(user_router, prefix="/user", tags=["user"])
api.include_router(websocket_router, prefix="/ws", tags=["websocket"])
app.include_router(api)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
