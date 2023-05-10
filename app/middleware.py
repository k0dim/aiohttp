import datetime
from typing import Callable, Awaitable

from aiohttp import web

from models import Token, get_session_maker
from mapping import raise_http_error
from crud import select_item
from config import TOKEN_TTL


@web.middleware
async def session_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    Session = get_session_maker()
    async with Session() as session:
        request["session"] = session
        return await handler(request)
    

@web.middleware
async def auth_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    token_id = request.headers.get("token")
    if not token_id:
        raise_http_error(web.HTTPForbidden, "incorrect token")
    try:
        token = await select_item(request["session"], Token, token_id)
    except web.HTTPNotFound:
        token = None
    if not token or token.created_at + datetime.timedelta(seconds=TOKEN_TTL) <= datetime.datetime.now():
        raise_http_error(web.HTTPForbidden, "incorrect token")
    request["token"] = token
    return await handler(request)