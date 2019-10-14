import logging

from datetime import datetime
from murakami.errors import ExporterError

logger = logging.getLogger(__name__)


class MurakamiExporter:
    def __init__(
            self,
            name="",
            location=None,
            network_type=None,
            connection_type=None,
            config=None,
    ):
        self.name = name
        self._location = location
        self._network_type = network_type
        self._connection_type = connection_type
        self._config = config

    def push(self, test_name="", data=None, timestamp=None):
        raise ExporterError(self.name, "No push() function implemented.")

    def _generate_filename(self, test_name="", timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

        if (self._location is not None and self._network_type is not None
                and self._connection_type is not None):
            return "%s-%s-%s-%s-%s.jsonl" % (
                test_name.lower(),
                self._location,
                self._network_type,
                self._connection_type,
                timestamp,
            )
        return "%s-%s.jsonl" % (test_name, timestamp)
