from fastapi import FastAPI

from .api import events
from .settings import get_settings


def init_app():
    settings = get_settings()
    new_app = FastAPI(title=settings.app_name, version=settings.app_version)

    new_app.include_router(events.router)

    return new_app


app = init_app()
