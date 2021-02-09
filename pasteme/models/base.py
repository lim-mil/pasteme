from peewee import Model, IntegerField, AutoField


class BaseModel(Model):
    id = AutoField(index=True, primary_key=True)
    created = IntegerField(index=True)
    updated = IntegerField(index=True)
