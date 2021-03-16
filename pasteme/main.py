import uvicorn
from pasteme.pkg.db import create_tables
from pasteme.pkg.redis import REDIS_POOL
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from pasteme import config
from pasteme.api.user import mount as user_monut
from pasteme.api.record import mount as record_mount
from pasteme.pkg.exception import handle_401
from pasteme.pkg.security_util import SecurityBackend


routes = [
    user_monut,
    record_mount,
    Mount('/meida', app=StaticFiles(directory='media'), name='media')
]


middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']),
    Middleware(AuthenticationMiddleware, backend=SecurityBackend(), on_error=handle_401),
]


on_startup = [
    create_tables,
    REDIS_POOL.connect,

]


on_shutdown = [

]


app = Starlette(debug=True, routes=routes, middleware=middleware, on_startup=on_startup, on_shutdown=on_shutdown, )


if __name__ == '__main__':
    uvicorn.run(app=app, host=config.HOST, port=config.PORT)
