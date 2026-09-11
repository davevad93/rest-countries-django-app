from django.apps import AppConfig
import logging
import os

logger = logging.getLogger(__name__)

class RestCountriesInfoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        if os.environ.get('PRELOAD_COUNTRIES_ON_STARTUP', '').lower() != 'true':
            return

        try:
            from .utils import get_cached_countries_data
            data = get_cached_countries_data()
            if data:
                logger.info("Preloaded countries data into cache (%s items).", len(data))
            else:
                logger.warning("Countries cache preload completed with empty dataset.")
        except Exception as exc:
            logger.exception("Countries cache preload failed: %s", exc)
