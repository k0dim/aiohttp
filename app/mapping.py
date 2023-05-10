import json
from typing import Type, Union
from datetime import datetime

from aiohttp import web


ERROR_TYPE = Union[
    Type[web.HTTPUnauthorized],
    Type[web.HTTPForbidden],
    Type[web.HTTPNotFound],
    Type[web.HTTPConflict],
    Type[web.HTTPBadRequest],
]

SUCCEED_TYPE = Union[
    Type[web.HTTPOk],
    Type[web.HTTPCreated],
    Type[web.HTTPNoContent],


]

def raise_http_error(error_class: ERROR_TYPE, message: str | dict):
    raise error_class(
        text=json.dumps({"status": "error", "description": message, "timemessage": datetime.now().isoformat()}),
        content_type="application/json",
    )


def raise_http_succeed(succeed_class: SUCCEED_TYPE, message: str | dict):
    return succeed_class(
        body=json.dumps({"status": "succeed", "description": message, "timemessage": datetime.now().isoformat()}),
        content_type="application/json",
    )