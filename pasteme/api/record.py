from typing import Optional

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route


# 权限，AuthCredentials 类的实例，在验证用户的中间件中提供。
from pasteme.models.record import record_model_manager, RecordModel, RECORD_STATUS


@requires('user')
async def records_list(request: Request):
    print(request.user.username)
    return PlainTextResponse(request.user.username, request.user.email)


@requires('user')
async def retrive_record(request: Request):
    # print(request.user.is_authenticated)
    print(request.auth.scopes)
    print(request.user.display_name)
    return PlainTextResponse(request.user.username + request.user.email)


@requires('user')
async def create_record(request: Request):
    record = await request.json()
    content = record.get('content')
    user_id = request.user.id
    await record_model_manager.create(content=content, user_id=user_id)
    return PlainTextResponse('ok')


@requires('user')
async def delete_record(request: Request):
    id = request.path_params['id']
    record: Optional[RecordModel] = await record_model_manager.get_or_none(id=id)
    if record:
        record.status = RECORD_STATUS.delete
        record.save()


@requires('user')
async def update_record(request: Request):
    id = request.path_params['id']
    record: Optional[RecordModel] = await record_model_manager.get_or_none(id=id)
    if record:
        body = await request.json()
        record.content = body.get('content', record.content)
        record.save()


# 路由参数，和 django 中的差不多，有五种类型——int、str、float、uuid、path
mount = Mount('/records', name='records', routes=[
    Route('/{id:int}', retrive_record, name='retrive', methods=['GET']),
    Route('/{id:int}', update_record, name='update', methods=['PATCH']),
    Route('', create_record, name='create', methods=['POST']),
    Route('', delete_record, name='delete', methods=['DELETE'])
])
