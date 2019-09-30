import logging
from webthing import Thing
from murakami.errors import RunnerError

logger = logging.getLogger(__name__)


class MurakamiRunner:
    def __init__(self, name="", config=None, data_cb=None):
        self.name = name
        self.config = config
        self.data_cb = data_cb
        self.thing = None
        self.is_ready = False

    async def _setup(self):
        raise RunnerError(self.name, "No _setup() function implemented.")

    async def setup(self):
        await self._setup()
        self.is_ready = True
        return

    async def _start_test(self):
        raise RunnerError(self.name, "No _start_test() function implemented.")

    async def start_test(self):
        if self.is_ready is False:
            await self.setup()
        data = await self._start_test()
        if self.data_cb is not None:
            self.data_cb(data)
        return data

    async def _stop_test(self):
        logger.debug("No special handling needed for stopping runner %s",
                     self.name)
        return

    async def stop_test(self):
        return self._stop_test()

    async def _teardown(self):
        logger.debug("No special teardown needed for runner %s", self.name)
        return

    async def teardown(self):
        await self._teardown()
        self.is_ready = False
        return

    @property
    def thing(self):
        return self.thing
