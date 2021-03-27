import base64
from typing import Optional

from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Mount, Route

from pasteme import config
from pasteme.models.UserModel import UserModel
from pasteme.pkg.response import resp
from pasteme.pkg.security_util import create_jwt_token
from pasteme.schemas.user import UserInCreate, UserInLogin
from pasteme.utils.email_util import send_email


async def login(reuqest: Request):
    user_info = await reuqest.json()
    username = user_info.get('username')
    password = user_info.get('password')
    user: Optional[UserModel] = UserModel.get_or_none(UserModel.username == username)
    if user and user.password == password:
        user_info['id'] = user.id
        result = {
            'token': create_jwt_token(user_info)
        }
        return resp(data=result)
    else:
        return resp(code=401, msg="用户名或密码错误")


async def register(request: Request):
    data = await request.json()
    try:
        user = UserInCreate(**data)
    except ValueError as e:
        return resp(code=401, msg='两次密码不一致')
    UserModel.create(**user.dict(exclude={'confirm_password'}))
    task = BackgroundTask(send_email, to_address=user.email, username=user.username)
    return resp(code=200, background=task)


async def checkout(request: Request):
    code = request.path_params.get('code')
    username = base64.b64decode(code).decode()
    user: Optional[UserModel] = UserModel.get_or_none(UserModel.username == username)
    user.status = 0
    user.save()
    jwt = create_jwt_token(UserInLogin.from_orm(user))
    return resp(code=200, data={'jwt_token': jwt})


mount = Mount('/users', name='users', routes=[
    Route('/login', login, methods=['POST'], name='login'),
    Route('/register', register, methods=['POST'], name='register'),
    Route('/checkout/{code:str}', checkout, methods=['GET'], name='checkout')
])
