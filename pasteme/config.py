import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

HOST = 'localhost'
PORT = 9999

REDIS_URI = 'redis://localhost:6379'
REDIS_DB = 0
REDIS_POOL_MAXSIZE = 30

try:
    if os.path.exists(os.path.join(BASE_DIR, 'private.py')):
        from .private import *
except Exception as e:
    pass
