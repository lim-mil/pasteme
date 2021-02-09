from peewee import CharField

from pasteme.models.base import BaseModel


class User(BaseModel):
    username = CharField(max_length=16, index=True)
    password = CharField(max_length=32, index=True)
    email = CharField(max_length=64, index=True)

    class Meta:
        table_name = 'user_model'
