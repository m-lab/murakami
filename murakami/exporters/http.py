import logging
import os
import json

import requests

from murakami.exporter import MurakamiExporter

logger = logging.getLogger(__name__)


class HTTPExporter(MurakamiExporter):
    """This exporter sends data to an HTTP endpoint."""
    def __init__(
            self,
            name="",
            location=None,
            network_type=None,
            connection_type=None,
            config=None,
    ):
        super().__init__(
            name=name,
            location=location,
            network_type=network_type,
            connection_type=connection_type,
            config=config,
        )
        logging.debug(config)
        self._url = config.get("url")

    def push(self, test_name="", data=None, timestamp=None):
        # Make a JSON payload with the expected format
        json_data = {
            'apiVersion': 1,
            'data': data
        }

        # POST the payload.
        resp = requests.post(self._url, data=json.dumps(json_data))
        if not resp.ok:
            logger.error("Exporting to HTTP endpoint failed: {}".format(
                resp.json()
            ))
            return False
        logger.info("Test data successfully sent to {}. Response: {}"
            .format(
                self._url,
                resp.json()
            ))
        return True
