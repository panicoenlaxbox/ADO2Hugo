import logging

from .version import __version__  # noqa: F401

logging.basicConfig(level=logging.DEBUG)

# https://stackoverflow.com/a/60823209
handler = logging.getLogger().handlers[0]
handler.addFilter(lambda record: (record.name != "urllib3.connectionpool"))
