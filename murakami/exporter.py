"""
This module includes the wrapper for all result exporters, which defines their
interface.
"""
import logging

from datetime import datetime
from murakami.errors import ExporterError

logger = logging.getLogger(__name__)

class MurakamiExporter:
    """
    MurakamiRunner is the superclass of all test runner plugins, and largely
    defines their interface to the rest of Murakami.

    ####Arguments
    * `name`: The name of this exporter
    * `device_id`: unique identifier for this Murakami device
    * `device_metadata1`: first user-defined metadata field
    * `device_metadata2`: second user-defined metadata field
    * `config`: A configuration dictionary passed to this instance from
    MurakamiServer
    """
    def __init__(
            self,
            name="",
            device_id=None,
            device_metadata1=None,
            device_metadata2=None,
            config=None,
    ):
        self.name = name
        self._device_id = device_id
        self._device_metadata1 = device_metadata1
        self._device_metadata2 = device_metadata2
        self._config = config

    def push(self, test_name="", data=None, timestamp=None):
        if type(data) is list:
            test_idx = 0
            for d in data:
                try:
                    self._push_single(test_name, d, timestamp, test_idx)
                    test_idx += 1
                except Exception as ex:
                    logger.error("export failed: " + ex)
                    return False
        else:
            return self._push_single(test_name, data, timestamp)

    def _push_single(self, test_name="", data=None, timestamp=None,
        test_idx=None):
        """
        Push results to this exporter (must be implemented by all exporters).

        ####Arguments
        * `test_name`: The name of this test.
        * `data`: A list of JSON objects containing test data.
        * `timestamp`: The timestamp of this test.
        """
        raise ExporterError(self.name, "No push() function implemented.")

    def _generate_filename(self, test_name="", timestamp=None,
        test_idx=None):
        if timestamp is None:
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        
        # If the result is part of a set of tests coming from a single runner,
        # these tests will have the same timestamp. To distinguish them and not
        # overwrite the same file N times, we append test_idx to the filename. 
        if test_idx is not None:
            timestamp = "%d-%s" % (test_idx, timestamp)


        if (self._device_id is not None and self._device_metadata1 is not None
                and self._device_metadata2 is not None):
            return "%s-%s-%s-%s-%s.jsonl" % (
                test_name.lower(),
                self._device_id,
                self._device_metadata1,
                self._device_metadata2,
                timestamp,
            )
        return "%s-%s.jsonl" % (test_name, timestamp)
