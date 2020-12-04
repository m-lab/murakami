import logging
import os

import jsonlines

import murakami.defaults as defaults
from murakami.exporter import MurakamiExporter

logger = logging.getLogger(__name__)


class LocalExporter(MurakamiExporter):
    """This exporter saves data to a local directory."""
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
        self._path = config.get("path", defaults.EXPORT_PATH)

    def _push_single(self, test_name="", data=None, timestamp=None,
        test_idx=None):
        try:
            dst_path = os.path.join(
                self._path, self._generate_filename(test_name, timestamp, test_idx))
            output = open(dst_path, "w")
            logger.info("Copying data to %s", dst_path)
            output.write(data)
        except Exception as err:
            logger.error("Exporting to local file failed: %s", err)
        else:
            output.close()
