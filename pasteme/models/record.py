from peewee import IntegerField, CharField, TextField

from pasteme.models.base import BaseModel


class RECORD_STATUS:
    normal: 0
    delete: 1


class Record(BaseModel):
    status = IntegerField(default=RECORD_STATUS.normal, index=True, help_text='状态')
    content = TextField(index=True, help_text='内容')
    user_id = IntegerField(index=True, help_text='创建者')

    class Meta:
        table_name = 'record_model'
