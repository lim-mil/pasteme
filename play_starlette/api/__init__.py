from starlette.applications import Starlette


def create_app():
    app = Starlette(
        debug=True,
    )