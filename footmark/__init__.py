
#
from footmark.pyami.config import Config, FootmarkConfigLocations
import datetime
import os
import platform
import re
import sys
import logging
import logging.config


__version__ = '2.42.0'
Version = __version__  # for backware compatibility

# http://bugs.python.org/issue7980
datetime.datetime.strptime('', '')

UserAgent = 'Footmark/%s Python/%s %s/%s' % (
    __version__,
    platform.python_version(),
    platform.system(),
    platform.release()
)
config = Config()

# Regex to disallow buckets violating charset or not [3..255] chars total.
BUCKET_NAME_RE = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9\._-]{1,253}[a-zA-Z0-9]$')
# Regex to disallow buckets with individual DNS labels longer than 63.
TOO_LONG_DNS_NAME_COMP = re.compile(r'[-_a-z0-9]{64}')
GENERATION_RE = re.compile(r'(?P<versionless_uri_str>.+)'
                           r'#(?P<generation>[0-9]+)$')
VERSION_RE = re.compile('(?P<versionless_uri_str>.+)#(?P<version_id>.+)$')
ENDPOINTS_PATH = os.path.join(os.path.dirname(__file__), 'endpoints.json')


def init_logging():
    for file in FootmarkConfigLocations:
        try:
            logging.config.fileConfig(os.path.expanduser(file))
        except:
            pass


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

log = logging.getLogger('footmark')
perflog = logging.getLogger('footmark.perf')
log.addHandler(NullHandler())
perflog.addHandler(NullHandler())
init_logging()

# convenience function to set logging to a particular file


def set_file_logger(name, filepath, level=logging.INFO, format_string=None):
    global log
    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.FileHandler(filepath)
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    log = logger


def set_stream_logger(name, level=logging.DEBUG, format_string=None):
    global log
    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.StreamHandler()
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    log = logger


def connect_ecs(acs_access_key_id=None, acs_secret_access_key=None, **kwargs):
    """
    :type acs_access_key_id: string
    :param acs_access_key_id: Your AWS Access Key ID

    :type acs_secret_access_key: string
    :param acs_secret_access_key: Your AWS Secret Access Key

    :rtype: :class:`footmark.ecs.connection.ECSConnection`
    :return: A connection to Amazon's ECS
    """
    from footmark.ecs.connection import ECSConnection
    return ECSConnection(acs_access_key_id, acs_secret_access_key, **kwargs)
