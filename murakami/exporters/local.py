import logging
import os

import jsonlines

import murakami.defaults as defaults
from murakami.exporter import MurakamiExporter

logger = logging.getLogger(__name__)


class LocalExporter(MurakamiExporter):
    """This exporter saves data to a local directory."""
    def __init__(self, name="", config=None, global_config=None):
        super().__init__(name=name, config=config, global_config=global_config)
        self._path = config.get("path", defaults.EXPORT_PATH)

    def push(self, test_name="", data=None, timestamp=None):
        try:
            dst_path = os.path.join(
                self._path,
                self._generate_filename(test_name, timestamp))
            output = open(dst_path, "w")
            logger.info("Copying data to %s", dst_path)
            with jsonlines.Writer(output) as writer:
                writer.write_all(data)
        except Exception as err:
            logger.error("Exporting to local file failed: %s", err)
        else:
            output.close()
