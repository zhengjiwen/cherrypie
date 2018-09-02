from .model import get_db
from .log import logging
import settings

# from .redis import r

db = get_db(settings.DB_COLLECTIONS, settings.DB_NAME, settings.DB_HOST)
logging = logging
