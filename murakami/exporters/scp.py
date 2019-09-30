import logging
import os

from paramiko import SSHClient
from paramiko.client import AutoAddPolicy
from scp import SCPClient


class SCPExporter:
    """This exporter allows to copy Murakami's data path to a remote host and
    folder via SCP."""
    def __init__(self, config):
        # Check if a configuration for the SCP exporter has been provided.
        self.config = config

        scp_config = self.config["push"]["scp"]
        self.target = scp_config.get("target", None)
        self.port = scp_config.get("port", 22)
        self.username = scp_config.get("username", None)
        self.password = scp_config.get("password", None)
        self.private_key = scp_config.get("private_key", None)

        self.run()

    def run(self):
        """Copy the files over SCP using the provided configuration."""
        if self.target is None:
            logging.error("scp.target must be specified")
            return

        if self.username is None and self.private_key is None:
            logging.error("scp.username or scp.private_key must be provided.")

        try:
            (dst_host, dst_path) = self.target.split(":")
        except ValueError:
            logging.error("scp.target must be 'host:/path/to/destination'")
            return

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy)
        ssh.connect(dst_host, self.port, username=self.username,
                    password=self.password, timeout=5)

        with SCPClient(ssh.get_transport()) as scp:
            # TODO: use actual data folder here
            dst_path = os.path.join("data", self.test_name)
            logging.info("Copying %s" % dst_path)
            scp.put(dst_path, recursive=True,
                    remote_path=self.dst_path)

        ssh.close()
