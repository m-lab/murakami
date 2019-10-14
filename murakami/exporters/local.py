import logging
import os

import jsonlines

import murakami.defaults as defaults
from murakami.exporter import MurakamiExporter

logger = logging.getLogger(__name__)


class LocalExporter(MurakamiExporter):
    """This exporter saves data to a local directory."""
    def __init__(self,
                 name="",
                 site=None,
                 location=None,
                 connection=None,
                 config=None):
        super().__init__(
            name=name,
            site=site,
            location=location,
            connection=connection,
            config=config,
        )
        self._path = config.get("path", defaults.EXPORT_PATH)

    def push(self, test_name="", data=None, timestamp=None):
        try:
            dst_path = os.path.join(
                self._path, self._generate_filename(test_name, timestamp))
            output = open(dst_path, "w")
            logger.info("Copying data to %s", dst_path)
            with jsonlines.Writer(output) as writer:
                writer.write_all(data)
        except Exception as err:
            logger.error("Exporting to local file failed: %s", err)
        else:
            output.close()
