import os
import subprocess
import logging
import time
import pytz

from datetime import datetime
from murakami.exporter import MurakamiExporter

logger = logging.getLogger(__name__)


class GCSExporter(MurakamiExporter):
    """This exporter allows to upload data to a Google Cloud Storage
    bucket."""
    def __init__(self, name="", config=None):
        super().__init__(name=name, config=config)
        self.target = config.get("target", None)
        self.service_account = config.get("service_account", None)
        self.key = config.get("key", None)

    def push(self, test_name="", data="", timestamp=None):
        """Upload the test data to GCS using the provided configuration."""
        if self.target is None:
            logger.error("GCS: target must be provided.")
            return
        if self.service_account is None or self.key is None:
            logger.error("GCS: a service account and key must be provided.")
            return

        # Configure the SDK to use the provided service account key.
        output = subprocess.run(["gcloud",
                                 "auth",
                                 "activate-service-account",
                                 self.service_account,
                                 "--key-file="+self.key],
                                check=True,
                                text=True,
                                capture_output=True)

        test_file = self._generate_filename(test_name, timestamp)
        tmp_path = "/tmp/" + test_file
        try:
            # Write content to a temporary file.
            with open(tmp_path, "w") as tmp_file:
                tmp_file.write(str(data))

            # Run gsutil to copy test data to the GCS bucket.
            output = subprocess.run([
                "gsutil",
                "cp",
                tmp_path,
                self.target + test_file
            ],
            check=True,
            text=True,
            capture_output=True)
        finally:
            # Make sure we remove the temporary file.
            os.remove(tmp_path)
