import logging
import os
import murakami.defaults as defaults
from murakami.errors import ExporterError

logger = logging.getLogger(__name__)


class MurakamiExporter:
    def __init__(self, name="", config=None):
        self.name = name
        self._config = config

    def push(self, test_name="", data=None, timestamp=None):
        raise ExporterError(self._name, "No push() function implemented.")

    def _generate_filename(self, test_name="", timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

        site = os.environ.get(defaults.ENV_SITE, None)
        device_loc = os.environ.get(defaults.ENV_DEVICE_LOC, None)
        conn_loc = os.environ.get(defaults.ENV_CONN_LOC, None)

        if (site is not None and device_loc is not None and
           connection_loc is not None):
            return "%s-%s-%s-%s-%s.jsonl" % (site, test_name, device_loc,
                                             conn_loc, timestamp)
        return "%s-%s.jsonl" % (test_name, timestamp)
