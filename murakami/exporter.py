import logging

from datetime import datetime
from murakami.errors import ExporterError

logger = logging.getLogger(__name__)


class MurakamiExporter:
    def __init__(self, name="", config=None, global_config=None):
        self.name = name
        self._config = config
        self._global_config = global_config

    def push(self, test_name="", data=None, timestamp=None):
        raise ExporterError(self._name, "No push() function implemented.")

    def _generate_filename(self, test_name="", timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

        if self._global_config.get("settings") is not None:
            site = self._global_config["settings"].get("site")
            device = self._global_config["settings"].get("device_location")
            connection = (self._global_config["settings"].
                          get("connection_location"))
            if (site is not None and device is not None and
               connection is not None):
                return "%s-%s-%s-%s-%s.jsonl" % (site, test_name, device,
                                                 connection, timestamp)
        return "%s-%s.jsonl" % (test_name, timestamp)
