from pasteme.pkg.db import MYSQL_DB
from pasteme.utils.time_util import get_current_ts
from peewee import Model, AutoField, IntegerField


class DatetimeMixin:
    create_at = IntegerField(default=get_current_ts)
    update_at = IntegerField(default=get_current_ts)


class BaseModel(Model, DatetimeMixin):
    id = AutoField(primary_key=True)

    class Meta:
        database = MYSQL_DB
