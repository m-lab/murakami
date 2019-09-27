import logging
import os

from paramiko import SSHClient
from paramiko.client import AutoAddPolicy
from scp import SCPClient


class SCPExporter:
    """This exporter allows to copy Murakami's data path to a remote host and
    folder via SCP."""
    def __init__(self, config):
        # XXX: this assumes the config for this exporter is at the root of the
        # config map. It's still undecided whether this is true or not.
        self.test_name = config['test']
        self.dst_host = config['host']
        self.dst_port = config['port']
        self.dst_path = config['remote_path']
        self.username = config.get('username', None)
        self.password = config.get('password', None)

    def run(self):
        """Copy the files over SCP using the provided configuration."""
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy)
        ssh.connect(self.dst_host, self.dst_port, username=self.username,
                    password=self.password)

        with SCPClient(ssh.get_transport()) as scp:
            # TODO: use actual data folder here
            dst_path = os.path.join("data", self.test_name)
            logging.info("Copying %s" % dst_path)
            scp.put(dst_path, recursive=True,
                    remote_path=self.dst_path)
            scp.close()
