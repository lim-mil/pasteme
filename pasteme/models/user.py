import asyncio

import peewee_async
from peewee import CharField

from pasteme.models.base import BaseModel, BaseManager
from pasteme.pkg.db import MYSQL_DB


class UserModel(BaseModel):
    username = CharField(max_length=16, index=True)
    password = CharField(max_length=32, index=True)
    email = CharField(max_length=64, index=True)

    class Meta:
        table_name = 'user_model'


# async
class UserModelManager(BaseManager):
    model = UserModel


user_model_manager = UserModelManager()
