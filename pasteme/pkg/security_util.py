import datetime
from typing import Optional

import jwt
from jwt import ExpiredSignatureError
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser, AuthenticationError
from starlette.requests import Request, HTTPConnection

from pasteme import config
from pasteme.pkg.response import resp_401


class SecurityBackend(AuthenticationBackend):
    """
    starlette 的用户验证，
    简陋，真的简陋...

    """
    async def authenticate(self, conn: HTTPConnection):
        global payload

        # 不需要走验证的请求，后续应该用正则表达式改一下
        if conn.url.path == '/users/login':
            return
        if conn.url.path.startswith('/records/') and conn.url.path != '/records/' and conn.get('method') == 'GET':
            return

        if 'Authorization' not in conn.headers:
            raise AuthenticationError()

        # 就直接从请求头拿 jwt token ...
        authorization = conn.headers.get('Authorization')
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
