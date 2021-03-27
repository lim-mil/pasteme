import datetime
from typing import Optional

import jwt
from jwt import ExpiredSignatureError
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser, AuthenticationError
from starlette.requests import Request, HTTPConnection

from pasteme import config
from pasteme.models.UserModel import UserModel


class SecurityBackend(AuthenticationBackend):
    """
    starlette 的用户验证，
    简陋，真的简陋...

    """
    async def authenticate(self, conn: HTTPConnection):
        global payload

        if conn.url.path == '/users/login' or conn.url.path == '/users/register':
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
        id = payload.get('id')

        user: Optional[UserModel] = UserModel.get_by_id(id)
        if user:
            return AuthCredentials(['user']), {'username': user.username, 'password': user.password}


def create_jwt_token(user_info):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'username': user_info.get('username'),
        'id': user_info.get('id')
    }
    token = jwt.encode(headers=headers, payload=payload, key=config.JWT_SECRET, algorithm='HS256')
    return token
