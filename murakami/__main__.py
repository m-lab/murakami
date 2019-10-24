"""
Murakami is a tool for creating an automated internet measurement service,
running in a Docker container. A Murakami measurement container can be
configured to automatically run supported tests four times a day using a
randomized schedule, and export each test result to a local storage device, to
one or more remote servers via SCP, or to a Google Cloud Storage bucket.
Results are saved as individual files in JSON new line format (.jsonl).
"""
from collections import ChainMap, OrderedDict
from collections.abc import Mapping
import logging
import os
import signal

import configargparse
import livejson
import tomlkit

import murakami.defaults as defaults
from murakami.server import MurakamiServer

logger = logging.getLogger(__name__)

config = None


def load_env():
    """This function loads the local environment into a dict and returns it."""
    acc = {}
    env = {k: v for k, v in os.environ.items() if k.startswith("MURAKAMI_")}

    def recurse(sec, value, acc):
        key = sec.pop(0)
        if sec:
            recurse(sec, value, acc.setdefault(key, {}))
        else:
            acc[key] = value

    for k, v in env.items():
        _, *sec = k.lower().split("_", 3)
        recurse(sec, v, acc)
    return acc


class TomlConfigFileParser(configargparse.ConfigFileParser):
    """
    This custom parser uses Tomlkit to parse a .toml configuration file,
    and then merges matching environment variables, and then puts then saves
    the result while passing back just the settings portion to configargparse.
    """
    def get_syntax_description(self):
        """Returns a description of the file format parsed by the class."""
        msg = ("Parses a TOML-format configuration file "
               "(see https://github.com/toml-lang/toml for the spec).")
        return msg

    def parse(self, stream):
        """
        Takes a TOML file stream and parses it, merging it with the
        environment, and then passes back just the settings portion.
        """
        global config
        config_file = tomlkit.parse(stream.read())
        config_env = load_env()
        config = {**config_file, **config_env}
        settings = OrderedDict()
        if "settings" in config:
            for key, value in config["settings"].items():
                settings[key] = str(value)

        return settings


def main():
    """ The main function for Murakami."""
    parser = configargparse.ArgParser(
        auto_env_var_prefix="murakami_settings_",
        config_file_parser_class=TomlConfigFileParser,
        default_config_files=defaults.CONFIG_FILES,
        description="The Murakami network test runner.",
        ignore_unknown_config_file_keys=True,
    )
    parser.add(
        "-c",
        "--config",
        is_config_file=True,
        required=False,
        help="Configuration file path (default: /etc/murakami/murakami.toml).",
    )
    parser.add(
        "-d",
        "--dynamic-state",
        default=defaults.DYNAMIC_FILE,
        dest="dynamic",
        help=
        "Path to dynamic configuration store, used to override settings via Webthings (default: /var/lib/murakami/config.json).",
    )
    parser.add(
        "-p",
        "--port",
        type=int,
        default=defaults.HTTP_PORT,
        help="The port to listen on for incoming connections (default: 80).",
    )
    parser.add("-n",
               "--hostname",
               help="The mDNS hostname for WebThings (default: automatic).")
    parser.add(
        "-s",
        "--ssl-options",
        nargs="?",
        dest="ssl_options",
        help="SSL options for the WebThings server (default: none).",
    )
    parser.add(
        "-r",
        "--additional-routes",
        nargs="?",
        dest="additional_routes",
        help="Additional routes for the WebThings server (default: none).",
    )
    parser.add(
        "-b",
        "--base-path",
        default="",
        dest="base_path",
        help="Base URL path to use, rather than '/' (default: '').",
    )
    parser.add(
        "-l",
        "--log",
        dest="loglevel",
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add(
        "-t",
        "--tests-per-day",
        dest="tests_per_day",
        type=int,
        default=defaults.TESTS_PER_DAY,
        help="Set the number of tests per day.",
    )
    parser.add(
        "-i",
        "--immediate",
        action="store_true",
        dest="immediate",
        default=False,
        help="Immediately run available tests on startup.",
    )
    parser.add(
        "-w",
        "--webthings",
        action="store_true",
        dest="webthings",
        default=False,
        help="Enable webthings support.",
    )
    parser.add(
        "--location",
        default=None,
        dest="location",
        help="Physical place Murakami node is located (default: '').",
    )
    parser.add(
        "--network-type",
        default=None,
        dest="network_type",
        help="Site associated with this Murakami node (default: '').",
    )
    parser.add(
        "--connection-type",
        default=None,
        dest="connection_type",
        help="Connection this associated with this node (default: '').",
    )
    settings = parser.parse_args()

    logging.basicConfig(
        level=settings.loglevel,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s",
    )

    global config
    if not config:
        config = load_env()
    if settings.webthings:
        state = livejson.File(settings.dynamic, pretty=True)
        config = ChainMap(state, config)

    server = MurakamiServer(
        port=settings.port,
        hostname=settings.hostname,
        ssl_options=settings.ssl_options,
        additional_routes=settings.additional_routes,
        base_path=settings.base_path,
        tests_per_day=settings.tests_per_day,
        immediate=settings.immediate,
        webthings=settings.webthings,
        location=settings.location,
        network_type=settings.network_type,
        connection_type=settings.connection_type,
        config=config,
    )

    # reload server on HUP and TERM signal
    signal.signal(signal.SIGHUP, server.reload)
    signal.signal(signal.SIGTERM, server.reload)

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
