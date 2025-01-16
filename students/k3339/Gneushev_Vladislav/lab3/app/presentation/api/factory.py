from fastapi import FastAPI

from app.presentation.api import middlewares
from app.presentation.api.exceptions import register_exception_handlers
from app.presentation.api.routes import register_routes


def create_bare_app() -> FastAPI:
    app = FastAPI()

    app.middleware("http")(middlewares.access_log_middleware)

    register_routes(app=app)
    register_exception_handlers(app=app)

    return app
