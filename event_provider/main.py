from fastapi import FastAPI

from event_provider.database import init_db

from . import models


def init_app():
    app = FastAPI(title="Ale.dev Test Challenge", version="0.0.1")
    init_db()


app = init_app()
