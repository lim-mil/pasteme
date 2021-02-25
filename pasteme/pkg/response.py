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


def resp_200(*, msg='', data=None) -> JSONResponse:
    content = ResponseContent(
        code=HTTPStatus.OK,
        msg=msg,
        data=data
    ).to_dict()
    return JSONResponse(content=content, status_code=HTTPStatus.OK)


def resp_404(*, msg='', data=None) -> JSONResponse:
    content = ResponseContent(
        code=HTTPStatus.NOT_FOUND,
        msg=msg,
        data=data
    ).to_dict()
    return JSONResponse(content=content, status_code=HTTPStatus.NOT_FOUND)


def resp_401(*, msg='', data=None) -> JSONResponse:
    content = ResponseContent(
        code=HTTPStatus.UNAUTHORIZED,
        msg=msg,
        data=data
    ).to_dict()
    return JSONResponse(content=content, status_code=HTTPStatus.UNAUTHORIZED)
