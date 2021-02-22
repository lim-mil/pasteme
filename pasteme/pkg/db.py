from peewee_async import MySQLDatabase


MYSQL_DB = MySQLDatabase('pasteme', **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'port': 3306,
                                        'user': 'root', 'password': '107382+1s'})


def create_table():
    from pasteme.models.user import UserModel
    from pasteme.models.record import RecordModel

    MYSQL_DB.connect()
    MYSQL_DB.create_tables([UserModel, RecordModel])
