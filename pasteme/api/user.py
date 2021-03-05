from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Mount, Route

from pasteme import config
from pasteme.pkg.response import resp_200
from pasteme.pkg.security_util import create_jwt_token


async def login(reuqest: Request):
    user_info = await reuqest.json()
    username = user_info.get('username')
    password = user_info.get('password')
    if username == config.USERNAME and password == config.PASSWORD:
        result = {
            'token': create_jwt_token(user_info)
        }
        return resp_200(data=result)


mount = Mount('/users', name='users', routes=[
    Route('/login', login, methods=['POST'], name='login'),
])
