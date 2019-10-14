from datetime import datetime
import logging

from webthing import Thing

from murakami.errors import RunnerError

logger = logging.getLogger(__name__)


class MurakamiRunner(Thing):
    def __init__(self,
                 id_,
                 title,
                 type_=[],
                 description="",
                 config=None,
                 data_cb=None):

        super().__init__(id_, title, type_, description)
        self._config = config
        self._data_cb = data_cb

    def _start_test(self):
        raise RunnerError(self.name, "No _start_test() function implemented.")

    def start_test(self):
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        data = self._start_test()
        if self._data_cb is not None:
            self._data_cb(test_name=self.title, data=data, timestamp=timestamp)
        return data

    def _stop_test(self):
        logger.debug("No special handling needed for stopping runner %s",
                     self.title)

    def stop_test(self):
        return self._stop_test()

    def _teardown(self):
        logger.debug("No special teardown needed for runner %s", self.title)

    def teardown(self):
        return self._teardown()
