import time
from typing import Union

from fastapi import HTTPException, status
from loguru import logger
from starlette.requests import Request


class DefaultException(HTTPException):
    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = "INTERNAL_SERVER_ERROR"
    MESSAGE: str
    ex: HTTPException
    data: Union[str, dict]

    def __init__(self, request: Request, data, **kwargs):
        process_time = (time.time() - request.state.start_time) * 1000  # Convert time to milliseconds
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)
        logger.bind(
            ip=request.state.ip,
            method="GET",
            statusCode=self.STATUS_CODE,
            path=request.url.path,
            response_time=f"{process_time:.2f}"
        ).error(data)
