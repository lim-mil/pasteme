import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')


HOST = 'localhost'
PORT = 9999

SQLITE_PATH = ''


try:
    if os.path.exists(os.path.join(BASE_DIR, 'private.py')):
        from .private import *
except Exception as e:
    pass
