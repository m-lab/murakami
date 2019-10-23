from datetime import datetime
import logging

from webthing import Thing

from murakami.errors import RunnerError
import murakami.utils as utils

logger = logging.getLogger(__name__)


class MurakamiRunner:
    def __init__(self, title, description="", config=None, data_cb=None):
        self.title = title
        self.description = description
        self._config = config
        self._data_cb = data_cb

    def _start_test(self):
        raise RunnerError(self.title, "No _start_test() function implemented.")

    def start_test(self):
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
        logger.debug("No special handling needed for stopping runner %s",
                     self.title)

    def stop_test(self):
        return self._stop_test()

    def _teardown(self):
        logger.debug("No special teardown needed for runner %s", self.title)

    def teardown(self):
        return self._teardown()

    @property
    def enabled(self):
        return utils.is_enabled(self._config.get("enabled", True))

    @enabled.setter
    def enabled(self, value):
        if bool(value):
            logger.debug("Enabling test %s", self.title)
            self._config["enabled"] = "y"
        else:
            logger.debug("Disabling test %s", self.title)
            self._config["enabled"] = "n"

    def set_enabled(self, value):
        self.enabled = value
