import logging
import os

import murakami.defaults as defaults
from murakami.exporter import MurakamiExporter

logger = logging.getLogger(__name__)


class LocalExporter(MurakamiExporter):
    """This exporter saves data to a local directory."""
    def __init__(
            self,
            name="",
            device_id=None,
            device_metadata1=None,
            device_metadata2=None,
            config=None,
    ):
        super().__init__(
            name=name,
            device_id=device_id,
            device_metadata1=device_metadata1,
            device_metadata2=device_metadata2,
            config=config,
        )
        logging.debug(config)
        self._path = config.get("path", defaults.EXPORT_PATH)

    def _push_single(self, test_name="", data=None, timestamp=None,
        test_idx=None):
        try:
            dst_path = os.path.join(
                self._path, self._generate_filename(test_name, timestamp, test_idx))
            logger.info("Copying data to %s", dst_path)
            with open(dst_path, "w") as output:
                output.write(data)
        except Exception as err:
            logger.error("Exporting to local file failed: %s", err)
