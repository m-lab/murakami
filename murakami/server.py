import logging
import pkg_resources
from webthing import WebThingServer, MultipleThings

logger = logging.getLogger(__name__)


class MurakamiServer:
    def __init__(
            self,
            port=80,
            hostname=None,
            ssl_options=None,
            additional_routes=None,
            base_path="",
            config=None,
    ):
        self.runners = {}

        for entry_point in pkg_resources.iter_entry_points("murakami.runners"):
            logging.debug("Loading plugin %s", entry_point.name)
            self.runners[entry_point.name] = entry_point.load()()

        self.server = WebThingServer(
            MultipleThings(self.runners.values(), "Murakami"),
            port=port,
            hostname=hostname,
            ssl_options=ssl_options,
            additional_routes=additional_routes,
            base_path=base_path,
        )

    def start(self):
        logger.info("Starting the WebThing server.")
        self.server.start()

    def stop(self):
        logger.info("Stopping the WebThing server.")
        self.server.stop()
