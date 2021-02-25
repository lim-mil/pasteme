import hashlib
import os
from json.decoder import JSONDecodeError
from typing import Optional

import aiofiles
from starlette.authentication import requires
from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Mount, Route


# 权限，AuthCredentials 类的实例，在验证用户的中间件中提供。
from pasteme.config import MEDIA_DIR
from pasteme.models.record import record_model_manager, RecordModel, records_users_model_manager, RecordsUsersModel
from pasteme.pkg.exception import RecordTypeError
from pasteme.pkg.response import resp_200, resp_404
from pasteme.schemas.record import RecordOut


@requires('user')
async def records_list(request: Request):
    """

    :param request:
    :return:
    """
    records_user = RecordsUsersModel.select().where(RecordsUsersModel.user_id==request.user.id, RecordsUsersModel.is_delete==False)
    result = []
    for i in records_user:
        record = await record_model_manager.get_or_none(RecordModel.id==i.record_id)
        if record:
            record_out = RecordOut.from_orm(record)
            record_out.id = i.id            # 这里的 id 也是 RecordsUsersModel 的 id！！！
            result.append(record_out.dict())
    return resp_200(data=result)


@requires('user')
async def retrive_record(request: Request):
    return PlainTextResponse(request.user.display_name)


@requires('user')
async def create_record(request: Request):
    """
    增加记录，如果记录内容相同（MD5），则在记录的数量加一。
    :param request:
    :return:
    """
    global file_content
    try:
        data = await request.json()
    except JSONDecodeError as e:
        data = await request.form()

    record_type = data.get('type', 'text')
    content = data.get('content')

    # 比对 md5
    hl = hashlib.md5()
    if record_type == 'text':
        hl.update(content.encode('utf-8'))
    elif record_type == 'file':
        file_content = await content.read()
        hl.update(file_content)
    else:
        raise RecordTypeError()

    record: Optional[RecordModel] = await record_model_manager.get_or_none(RecordModel.md5==hl.hexdigest())
    if record:
        record.num += 1
        record.save()
        await records_users_model_manager.create(user_id=request.user.id, record_id=record.id)
        return resp_200()

    # 存储文件
    if record_type == 'file':
        content = content.filename
        async with aiofiles.open(os.path.join(MEDIA_DIR, content), mode='wb') as f:
            await f.write(file_content)

    await record_model_manager.create(content=content, md5=hl.hexdigest(), type=record_type, num=1)
    record = await record_model_manager.get_or_none(RecordModel.md5==hl.hexdigest())
    await records_users_model_manager.create(user_id=request.user.id, record_id=record.id)

    return resp_200()


@requires('user')
async def delete_record(request: Request):
    """
    这里的 id，都是 RecordsUsersModel 的 id，因为只有它的id是唯一的
    :param request:
    :return:
    """
    id = request.path_params['id']
    record_user: Optional[RecordsUsersModel] = await records_users_model_manager.get_or_none(RecordsUsersModel.id==id)
    if record_user:
        record: Optional[RecordModel] = await record_model_manager.get_or_none(RecordModel.id==record_user.record_id)
        if record:
            record.num -= 1
            record.save()
        record_user.is_delete = True
        record_user.save()
    else:
        return resp_404()
    return resp_200()


@requires('user')
async def update_record(request: Request):
    id = request.path_params['id']
    record_user: Optional[RecordsUsersModel] = await records_users_model_manager.get_or_none(RecordsUsersModel.id==id)
    if record_user:
        body = await request.json()
        record: Optional[RecordModel] = await record_model_manager.get_or_none(RecordModel.id==record_user.record_id)
        if record:
            record.content = body.get('content', record.content)
            record.save()
            return resp_200()
    return resp_404()


# 路由参数，和 django 中的差不多，有五种类型——int、str、float、uuid、path
mount = Mount('/records', name='records', routes=[
    Route('/', create_record, name='create', methods=['POST']),
    Route('/', records_list, name='list', methods=['GET']),
    Route('/{id:int}', retrive_record, name='retrive', methods=['GET']),
    Route('/{id:int}', update_record, name='update', methods=['PATCH']),
    Route('/{id:int}', delete_record, name='delete', methods=['DELETE'])
])
