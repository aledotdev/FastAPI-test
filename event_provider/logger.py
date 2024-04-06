import logging

import coloredlogs

from event_provider.settings import get_settings

settings = get_settings()

logger = logging.root
handler = logging.StreamHandler()
# handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(settings.LOG_LEVEL)

if settings.ENV == "dev":
    coloredlogs.install(level=settings.LOG_LEVEL)
