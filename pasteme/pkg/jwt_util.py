import datetime

import jwt

from pasteme import config
from pasteme.models.user import UserModel


def create_jwt_token(user: UserModel):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'username': user.username
    }
    token = jwt.encode(headers=headers, payload=payload, key=config.JWT_SECRET, algorithm='HS256')
    return token
