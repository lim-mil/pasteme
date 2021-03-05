from enum import Enum

import aioredis
from aioredis import Redis
from pasteme import config


class RedisPool:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await aioredis.create_pool(config.REDIS_URI, db=config.REDIS_DB, encoding='utf-8',
                                               maxsize=config.REDIS_POOL_MAXSIZE)


REDIS_POOL = RedisPool()


class GetRedis():
    async def __aenter__(self):
        self.conn = await REDIS_POOL.pool.acquire()
        self.redis = Redis(self.conn)
        return self.redis

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        REDIS_POOL.pool.release(self.conn)


# 用到的 redis 表名(姑且称为表...)
class RedisTBName(Enum):
    USERS_HASHES = 'pasteme_users_hashes'
    MD5_HASHES = 'pasteme_md5_hashes'           # md5: 存储的文件名
    FILENAME_SETS = 'pasteme_filename_sets'         # 已存在的文件名
    FILEINFO_HASHES = 'pasteme_fileinfo_hashes'         #
    FILEID_SETS = 'pasteme_fileid_sets'         # 文件 id

