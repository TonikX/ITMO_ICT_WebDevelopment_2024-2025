import logging
from functools import partial

from dishka import make_async_container, AsyncContainer
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI

from app.config.provider import ConfigProvider
from app.config.models import Config
from app.config.parser import load_config
from app.infrastructure.database.provider import DatabaseProvider
from app.log import setup_logging
from app.presentation.api.factory import create_bare_app

from app.services.provider import ServiceProvider

logger = logging.getLogger(__name__)


async def on_shutdown(container: AsyncContainer):
    await container.close()


def create_app() -> FastAPI:
    setup_logging()

    config = load_config(
        config_class=Config,
        env_file_path=".env"
    )
    app = create_bare_app()
    container = make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        ServiceProvider(),
        context={Config: config}
    )

    fastapi_integration.setup_dishka(container=container, app=app)

    teardown = partial(on_shutdown, container)
    app.add_event_handler("shutdown", teardown)

    return app
