from http import HTTPStatus
from typing import Any

from starlette.responses import JSONResponse


class ResponseContent:
    code: int
    data: Any
    msg: str

    def __init__(self, *, code: int, msg: str, data: Any):
        self.code = code
        self.data = data
        self.msg = msg

    def to_dict(self):
        return {
            'code': self.code,
            'msg': self.msg,
            'data': self.data
        }


def resp(*, code=200, msg='', data=None, **kwargs) -> JSONResponse:
    content = ResponseContent(
        code=code,
        msg=msg,
        data=data
    ).to_dict()
    return JSONResponse(content=content, status_code=code, **kwargs)
