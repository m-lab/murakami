import logging
from murakami.errors import ExporterError

logger = logging.getLogger(__name__)


class MurakamiExporter:
    def __init__(self, name="", config=None):
        self._name = name
        self._config = config

    def push(self, test_name="", data="", timestamp=None):
        raise ExporterError(self._name, "No push() function implemented.")
