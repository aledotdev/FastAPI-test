from fastapi import FastAPI

from event_provider.database import init_db

from . import models  # pylint: disable=unused-import


def init_app():
    new_app = FastAPI(title="Ale.dev Test Challenge", version="0.0.1")
    init_db()
    return new_app


app = init_app()
