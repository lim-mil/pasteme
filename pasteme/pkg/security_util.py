import datetime
from typing import Optional

import jwt
from jwt import ExpiredSignatureError
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser, AuthenticationError
from starlette.requests import Request

from pasteme import config
from pasteme.pkg.response import resp_401


class SecurityBackend(AuthenticationBackend):
    """
    starlette 的用户验证，
    简陋，真的简陋...

    """
    async def authenticate(self, request: Request):
        global payload

        if request.url.path == '/users/login':
            return

        if 'Authorization' not in request.headers:
            raise AuthenticationError()

        # 就直接从请求头拿 jwt token ...
        authorization = request.headers.get('Authorization')
        token = authorization.split(' ')[1]
        try:
            payload = jwt.decode(token, algorithms=['HS256'], key=config.JWT_SECRET)
        except ExpiredSignatureError:
            pass
        username = payload.get('username')

        if username == config.USERNAME:
            return AuthCredentials(['user']), {'username': config.USERNAME, 'password': config.PASSWORD}


def create_jwt_token(user_info):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'username': user_info.get('username')
    }
    token = jwt.encode(headers=headers, payload=payload, key=config.JWT_SECRET, algorithm='HS256')
    return token
