from peewee import Model, IntegerField, AutoField

from pasteme.pkg.db import MYSQL_DB


class BaseModel(Model):
    id = AutoField(index=True, primary_key=True)
    created = IntegerField(index=True)
    updated = IntegerField(index=True)

    class Meta:
        database = MYSQL_DB
