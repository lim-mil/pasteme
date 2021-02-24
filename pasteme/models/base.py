from typing import Optional

import peewee_async
from peewee import Model, IntegerField, AutoField, DoesNotExist, BooleanField
from starlette.authentication import BaseUser

from pasteme.pkg.db import MYSQL_DB
from pasteme.utils.time_util import get_current_ts


class BaseModel(Model):
    id = AutoField(index=True, primary_key=True)
    created_at = IntegerField(index=True, default=get_current_ts)
    updated_at = IntegerField(index=True, default=get_current_ts)
    is_delete = BooleanField(index=True, default=False)

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
        return await self.manager.get(self.model, self.model.id==id)

    async def create(self, **kwargs):
        return await self.manager.create(self.model, **kwargs)

    async def get_or_none(self, *args):
        try:
            return await self.manager.get(self.model, *args)
        except DoesNotExist:
            return None

    async def delete_by_id(self, id):
        obj = await self.get_by_id(id)
        if obj:
            await self.manager.delete(obj)


class AuthUser(BaseUser):
    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username
