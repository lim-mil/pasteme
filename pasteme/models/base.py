from typing import Optional

import peewee_async
from peewee import Model, IntegerField, AutoField, DoesNotExist

from pasteme.pkg.db import MYSQL_DB
from pasteme.utils.time_util import get_current_ts


class BaseModel(Model):
    id = AutoField(index=True, primary_key=True)
    created = IntegerField(index=True, default=get_current_ts)
    updated = IntegerField(index=True, default=get_current_ts)

    class Meta:
        database = MYSQL_DB


class BaseManager:
    db = MYSQL_DB
    _manager = None

    def __init__(self):
        self._manager = peewee_async.Manager(self.db)

    @property
    def manager(self):
        return self._manager

    async def get_by_id(self, id):
        """
        将一些基本操作封装为异步的形式
        :param id:
        :return:
        """
        return await self.manager.get(self.model, id=id)

    async def create(self, **kwargs):
        return await self.manager.create(self.model, **kwargs)

    async def get_or_none(self, **kwargs):
        try:
            return await self.manager.get(self.model, **kwargs)
        except DoesNotExist:
            return None