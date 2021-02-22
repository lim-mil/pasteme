from peewee_async import MySQLDatabase

from pasteme import config


# peewee async
MYSQL_DB = MySQLDatabase(config.DB_NAME, **{'charset': 'utf8', 'use_unicode': True, 'host': config.DB_HOST, 'port': config.DB_PORT,
                                        'user': config.DB_USER, 'password': config.DB_PASSWORD})


def create_table():
    from pasteme.models.user import UserModel
    from pasteme.models.record import RecordModel

    MYSQL_DB.connect()
    MYSQL_DB.create_tables([UserModel, RecordModel])
