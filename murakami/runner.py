from datetime import datetime
import logging
from murakami.errors import RunnerError

logger = logging.getLogger(__name__)


class MurakamiRunner:
    def __init__(self, name="", config=None, data_cb=None):
        self.name = name
        self._config = config
        self._data_cb = data_cb
        self.thing = None

    def _start_test(self):
        raise RunnerError(self.name, "No _start_test() function implemented.")

    def start_test(self):
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        data = self._start_test()
        if self._data_cb is not None:
            self._data_cb(test_name=self.name, data=data, timestamp=timestamp)
        return data

    def _stop_test(self):
        logger.debug("No special handling needed for stopping runner %s",
                     self.name)

    def stop_test(self):
        return self._stop_test()

    def _teardown(self):
        logger.debug("No special teardown needed for runner %s", self.name)

    def teardown(self):
        return self._teardown()
