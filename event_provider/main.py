from fastapi import FastAPI

from event_provider.database import create_async_engine, init_db
from event_provider.settings import get_settigns


def init_app():
    settings = get_settigns()
    new_app = FastAPI(title=settings.app_name, version=settings.app_version)
    init_db(create_async_engine(settings))
    return new_app


app = init_app()
