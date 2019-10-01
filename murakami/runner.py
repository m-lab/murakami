import logging
from webthing import Thing
from murakami.errors import RunnerError

logger = logging.getLogger(__name__)


class MurakamiRunner:
    def __init__(self, name="", config={}, data_cb=None):
        self.name = name
        self.config = config
        self.data_cb = data_cb
        self._thing = None

    def _start_test(self):
        raise RunnerError(self.name, "No _start_test() function implemented.")

    def start_test(self):
        data = self._start_test()
        if self.data_cb is not None:
            self.data_cb(data)
        return data

    def _stop_test(self):
        logger.debug("No special handling needed for stopping runner %s",
                     self.name)
        return

    def stop_test(self):
        return self._stop_test()

    def _teardown(self):
        logger.debug("No special teardown needed for runner %s", self.name)
        return

    def teardown(self):
        self._teardown()
        self.is_ready = False
        return

    @property
    def thing(self):
        return self._thing
