import re

EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/)"


async def check_request_url(url):
    result = re.match(EXCEPT_PATH_REGEX, url)
    return result or url in EXCEPT_PATH_LIST
