import logging

from datetime import datetime
from murakami.errors import ExporterError

logger = logging.getLogger(__name__)


class MurakamiExporter:
    def __init__(self,
                 name="",
                 site=None,
                 location=None,
                 connection=None,
                 config=None):
        self.name = name
        self._site = site
        self._location = location
        self._connection = connection
        self._config = config

    def push(self, test_name="", data=None, timestamp=None):
        raise ExporterError(self.name, "No push() function implemented.")

    def _generate_filename(self, test_name="", timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

        if (self._site is not None and self._location is not None
                and self._connection is not None):
            return "%s-%s-%s-%s-%s.jsonl" % (
                self._site,
                test_name.lower(),
                self._location,
                self._connection,
                timestamp,
            )
        return "%s-%s.jsonl" % (test_name, timestamp)
