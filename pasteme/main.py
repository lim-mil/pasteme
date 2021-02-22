import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route

from pasteme import config
from pasteme.pkg.db import create_table
from pasteme.api.user import mount as user_monut


routes = [
    user_monut,
]


middleware = [

]


on_startup = [
    create_table
]


on_shutdown = [

]


app = Starlette(debug=True, routes=routes, middleware=middleware, on_startup=on_startup, on_shutdown=on_shutdown, )


if __name__ == '__main__':
    uvicorn.run(app=app, host=config.HOST, port=config.PORT)
