import hashlib
import os
from json.decoder import JSONDecodeError
from typing import Optional

import aiofiles
from pasteme.pkg.redis import GetRedis, RedisTBName
from pasteme.utils.name_util import give_me_a_name
from starlette.authentication import requires
from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse, FileResponse
from starlette.routing import Mount, Route


# 权限，AuthCredentials 类的实例，在验证用户的中间件中提供。
from pasteme.config import MEDIA_DIR
from pasteme.pkg.exception import RecordTypeError
from pasteme.pkg.response import resp
from pasteme.schemas.record import RecordOut


@requires('user')
async def create_record(request: Request):
    """
    增加记录，如果记录内容相同（MD5），则在记录的数量加一。
    :param request:
    :return:
    """
    async with GetRedis() as redis:
        data = await request.form()
        file: UploadFile = data.get('file')
        file_subname = file.filename.split('.')[-1]
        hl = hashlib.md5()

        content = await file.read()
        hl.update(content)
        md5 = hl.hexdigest()
        print(md5)
        if await redis.hexists(RedisTBName.MD5_HASHES.value, md5):
            filename_server = await redis.hget(RedisTBName.MD5_HASHES.value, md5)
        else:
            filename_server = await give_me_a_name()
            await redis.hset(RedisTBName.MD5_HASHES.value, md5, filename_server)
            async with aiofiles.open(os.path.join(MEDIA_DIR, filename_server), mode='wb') as f:
                await f.write(content)
        id = await give_me_a_name()
        await redis.sadd(RedisTBName.FILEID_SETS.value, id)
        await redis.hset(id, 'md5', md5)
        await redis.hset(id, 'filename', file.filename)

    return resp(code=200, data={'id': id})


async def retrive_record(request: Request):
    async with GetRedis() as redis:
        id = request.path_params['id']
        md5 = await redis.hget(id, 'md5')
        filename_server = await redis.hget(RedisTBName.MD5_HASHES.value, md5)
        if filename_server:
            return FileResponse(os.path.join(MEDIA_DIR, filename_server), filename=await redis.hget(id, 'filename'))


@requires('user')
async def retrive_reocrds(request: Request):
    result = []
    async with GetRedis() as redis:
        id_list = await redis.smembers(RedisTBName.FILEID_SETS.value)
        for id in id_list:
            item = {}
            item['id'] = id
            item['filename'] = await redis.hget(id, 'filename')
            result.append(item)
    return resp(code=200, data=result)


# 路由参数，和 django 中的差不多，有五种类型——int、str、float、uuid、path
mount = Mount('/records', name='records', routes=[
    Route('/', create_record, name='create', methods=['POST']),
    Route('/', retrive_reocrds, name='retrive_list', methods=['GET']),
    Route('/{id:str}', retrive_record, name='retrive', methods=['GET']),
])
