from typing import Optional

from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Mount, Route

from pasteme.models.user import user_model_manager, UserModel
from pasteme.pkg.response import resp_200
from pasteme.pkg.security_util import create_jwt_token


async def register(request: Request):
    user_info = await request.form()
    username = user_info.get('username')
    password = user_info.get('password')
    re_password = user_info.get('re_password')
    email = user_info.get('email')
    if password != re_password:
        pass
    await user_model_manager.create(username=username, password=password, email=email)
    return PlainTextResponse("ok")


async def login(reuqest: Request):
    user_info = await reuqest.json()
    email = user_info.get('email')
    password = user_info.get('password')
    user: Optional[UserModel] = await user_model_manager.get_or_none(UserModel.email==email, UserModel.password==password)
    if user:
        result = {
            'token': create_jwt_token(user),
            'username': user.username
        }
        return resp_200(data=result)


# 与 django 的 include、fastapi 的 APIRoute 差不多
mount = Mount('/users', name='users', routes=[
    Route('/register', register, methods=['POST'], name='register'),
    Route('/login', login, methods=['POST'], name='login'),

])

