
import os
import logging


ROOT_DIR = os.path.dirname(__file__)

LOG_LEVEL = logging.DEBUG

CACHE_LIMIT = 20


CACHE_FILE_PATH = os.path.join(ROOT_DIR, "cache", "cache.pickle")
if not os.path.exists(os.path.dirname(CACHE_FILE_PATH)):
    try:
        os.makedirs(os.path.dirname(CACHE_FILE_PATH))
    except:
        pass


SAMPLE_DATA = os.path.join(ROOT_DIR, 'sample', 'data.json')
