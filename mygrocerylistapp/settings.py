import logging
import os

logger = logging.getLogger(__name__)

if 'DJANGO_SETTINGS' in os.environ:
    if os.environ['DJANGO_SETTINGS'] == "dev":
        logger.debug("DEV SERVER")
        from .settings_dev import *
else:
    logger.debug("PROD SERVER")
    from .settings_prod import *