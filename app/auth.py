import bcrypt
from aiohttp import web

from mapping import raise_http_error

from logger import py_logger


def hash_password(password: str):
    py_logger.info("hash password")
    return (bcrypt.hashpw(password.encode(), bcrypt.gensalt())).decode()


def check_password(password: str, hashed_password: str):
    py_logger.info("check password")
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def check_owner(request: web.Request, user_id: int):
    py_logger.info("check owner")
    if not request["token"] or request["token"].user.id != user_id:
        py_logger.error("only owner has access")
        raise_http_error(web.HTTPForbidden, "only owner has access")