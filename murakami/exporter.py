"""
This module includes the wrapper for all result exporters, which defines their
interface.
"""
from datetime import datetime
from murakami.errors import ExporterError


class MurakamiExporter:
    """
    MurakamiRunner is the superclass of all test runner plugins, and largely
    defines their interface to the rest of Murakami.

    ####Arguments
    * `name`: The name of this exporter
    * `location`: string describing physical location of this device
    * `network_type`: string describing the network this device is connected to
    * `connection_type`: string describing type of connection this device is
    using
    * `config`: A configuration dictionary passed to this instance from
    MurakamiServer
    """
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
        """
        Push results to this exporter (must be implemented by all exporters).

        ####Arguments
        * `test_name`: The name of this test.
        * `data`: A list of JSON objects containing test data.
        * `timestamp`: The timestamp of this test.
        """
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
