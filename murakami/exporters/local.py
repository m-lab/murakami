import logging
import os

import jsonlines

import murakami.defaults as defaults
from murakami.exporter import MurakamiExporter

logger = logging.getLogger(__name__)


class LocalExporter(MurakamiExporter):
    """This exporter saves data to a local directory."""
    def __init__(self, name="", config=None):
        super().__init__(name=name, config=config)
        self._path = config.get("path", defaults.EXPORT_PATH)

    def push(self, test_name="", data=None, timestamp=None):
        try:
            dst_path = os.path.join(
                self._path,
                str(test_name) + "-" + str(timestamp) + ".jsonl")
            output = open(dst_path, "w")
            logger.info("Copying data to %s", dst_path)
            with jsonlines.Writer(output) as writer:
                writer.write_all(data)
        except Exception as err:
            logger.error("Exporting to local file failed: %s", err)
        else:
            output.close()
