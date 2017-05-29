
import logging
import settings


def get_logger(loglevel=settings.LOG_LEVEL):
    _ = logging.getLogger()
    _.setLevel(loglevel)

    ch = logging.StreamHandler()
    ch.setLevel(loglevel)

    formatter = logging.Formatter('%(asctime)s [%(levelname)8s] - %(message)s')

    ch.setFormatter(formatter)

    _.addHandler(ch)

    return _

log = get_logger()