from peewee import IntegerField, CharField, TextField

from pasteme.models.base import BaseModel, BaseManager


class RecordsUsersModel(BaseModel):
    user_id = IntegerField(index=True, help_text='用户')
    record_id = IntegerField(index=True, help_text='记录')

    class Meta:
        table_name = 'records_users_model'


class RecordsUsersModelManager(BaseManager):
    model = RecordsUsersModel


records_users_model_manager = RecordsUsersModelManager()


class RecordModel(BaseModel):
    content = TextField(help_text='内容，对于文件而言就是原文件名')
    md5 = CharField(max_length=1024, index=True, help_text='MD5')
    type = CharField(max_length=16, index=True, help_text='类型')
    num = IntegerField(default=0, index=True, help_text='数量')

    class Meta:
        table_name = 'record_model'


class RecordModelManager(BaseManager):
    model = RecordModel


record_model_manager = RecordModelManager()
