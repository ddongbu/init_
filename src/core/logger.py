import os

from loguru import logger


def init_logger():
    log_path = "/log/scheduler_{time:YYYYMMDD}.log"
    logger.remove()
    logger.add(
        sink=f"{os.getcwd()}{log_path}",
        format="{time:YYYY-MM-DD HH:mm:ss} [{extra[response_time]}ms] | "
               '[{level}] | {extra[ip]} | {extra[statusCode]} {extra[method]} "{extra[path]}" | {message}',
        rotation="00:00",
        retention="14 days",
        level="DEBUG",
        compression="gz",
        backtrace=False,
        diagnose=False,
    )
