import io
import logging
import os

import jsonlines
from paramiko import SSHClient
from paramiko.client import AutoAddPolicy
from scp import SCPClient

import murakami.defaults as defaults
from murakami.exporter import MurakamiExporter

logger = logging.getLogger(__name__)


class SCPExporter(MurakamiExporter):
    """This exporter allows to copy Murakami's data path to a remote host and
    folder via SCP."""
    def __init__(self, name="", config=None):
        # Check if a configuration for the SCP exporter has been provided.
        super().__init__(name=name, config=config)
        self.target = config.get("target", None)
        self.port = config.get("port", defaults.SSH_PORT)
        self.username = config.get("username", None)
        self.password = config.get("password", None)
        self.private_key = config.get("private_key", None)

    def push(self, test_name="", data=None, timestamp=None):
        """Copy the files over SCP using the provided configuration."""
        if self.target is None:
            logger.error("scp.target must be specified")
            return

        if self.username is None and self.private_key is None:
            logging.error("scp.username or scp.private_key must be provided.")

        try:
            (dst_host, dst_path) = self.target.split(":")
        except ValueError:
            logger.error("scp.target must be 'host:/path/to/destination'")
            return

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy)

        try:
            ssh.connect(
                dst_host,
                self.port,
                username=self.username,
                password=self.password,
                timeout=defaults.SSH_TIMEOUT,
            )

            with SCPClient(ssh.get_transport()) as scp:
                dst_path = os.path.join(dst_path,
                                        test_name + "-" + timestamp + ".jsonl")
                logger.info("Copying data to %s", dst_path)
                buf = io.StringIO()
                with jsonlines.open(buf, mode="w") as writer:
                    writer.write_all(data)
                scp.putfo(buf, dst_path)
        except Exception as err:
            logger.error("SCP exporter failed: %s", err)
        else:
            ssh.close()
