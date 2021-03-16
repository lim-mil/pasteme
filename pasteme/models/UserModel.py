from pasteme.models.BaseModel import BaseModel
from peewee import CharField, IntegerField


class UserModel(BaseModel):
    username = CharField(max_length=64, unique=True, help_text='用户名')
    email = CharField(max_length=128, help_text='邮箱')
    password = CharField(max_length=64, help_text='密码')
    status = IntegerField(default=1, help_text='状态')
