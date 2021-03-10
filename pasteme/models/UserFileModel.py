from pasteme.models.BaseModel import BaseModel
from peewee import IntegerField, CharField


class UserFileModel(BaseModel):
    user_id = IntegerField()
    file_id = CharField(max_length=256)
