"""
This module includes the wrapper for all test runners, which defines their
interface.
"""
from datetime import datetime
import logging

from webthing import Thing

from murakami.errors import RunnerError
import murakami.utils as utils

_logger = logging.getLogger(__name__)


class MurakamiRunner:
    """
    MurakamiRunner is the superclass of all test runner plugins, and largely
    defines their interface to the rest of Murakami.

    ####Arguments
    * `title`: The name of this runner
    * `description`: A string describing this runner
    * `config`: A configuration dictionary passed to this instance from
    MurakamiServer
    * `data_cb`: The callback function that receives the test results
    """
    def __init__(self, title, description="", config=None, data_cb=None,
        location=None, network_type=None, connection_type=None,
        device_id=None):
        self.title = title
        self.description = description
        self._config = config
        self._data_cb = data_cb
        self._location = location
        self._network_type = network_type
        self._connection_type = connection_type
        self._device_id = device_id

    def _start_test(self):
        raise RunnerError(self.title, "No _start_test() function implemented.")

    def start_test(self):
        """Starts this test, wraps the actual start function."""
        if self.enabled:
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
            data = self._start_test()
            if self._data_cb is not None:
                self._data_cb(test_name=self.title,
                              data=data,
                              timestamp=timestamp)
            return data
        logging.info("Test runner %s disabled, skipping.", self.title)

    def _stop_test(self):
        _logger.debug("No special handling needed for stopping runner %s",
                      self.title)

    def stop_test(self):
        """Stops this test, wraps the actual stop function (optional)."""
        return self._stop_test()

    def _teardown(self):
        _logger.debug("No special teardown needed for runner %s", self.title)

    def teardown(self):
        """Any final deconstruction for this runner (optional)."""
        return self._teardown()

    @property
    def enabled(self):
        """Property describing whether this test is enabled."""
        return utils.is_enabled(self._config.get("enabled", True))

    @enabled.setter
    def enabled(self, value):
        if bool(value):
            _logger.debug("Enabling test %s", self.title)
            self._config["enabled"] = "y"
        else:
            _logger.debug("Disabling test %s", self.title)
            self._config["enabled"] = "n"

    def set_enabled(self, value):
        """Sets whether this test is enabled."""
        self.enabled = value
