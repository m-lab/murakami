from collections import OrderedDict
import logging
import os
import configargparse
import tomlkit
from murakami.server import MurakamiServer

config = None


def load_env():
    acc = {}
    env = {k: v for k, v in os.environ.items() if k.startswith("MURAKAMI_")}

    def recurse(key, value, acc):
        key, *re = key.split("_", 1)
        if re:
            recurse(re[0], value, acc.setdefault(key.lower(), {}))
        else:
            acc[key.lower()] = value

    for k, v in env.items():
        recurse(k, v, acc)
    if "murakami" in acc:
        return acc["murakami"]
    else:
        return {}


class TomlConfigFileParser(configargparse.ConfigFileParser):
    def get_syntax_description(self):
        msg = ("Parses a TOML-format configuration file "
               "(see https://github.com/toml-lang/toml for the spec).")
        return msg

    def parse(self, stream):
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
    parser = configargparse.ArgParser(
        auto_env_var_prefix="murakami_settings_",
        config_file_parser_class=TomlConfigFileParser,
        default_config_files=[
            "/murakami/murakami.toml",
            "~/.config/murakami/murakami.toml",
        ],
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
        "-p",
        "--port",
        type=int,
        default=80,
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
        default=2,
        help="Set the number of tests per day.",
    )
    parser.add(
        "-e",
        "--expected-sleep-seconds",
        dest="expected_sleep_seconds",
        type=int,
        default=12 * 60 * 60,
        help="Set the minimum number of seconds between random tests.",
    )
    settings = parser.parse_args()

    logging.basicConfig(
        level=settings.loglevel,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s",
    )

    global config
    if not config:
        config = load_env()

    server = MurakamiServer(
        port=settings.port or 8080,
        hostname=settings.hostname,
        ssl_options=settings.ssl_options,
        additional_routes=settings.additional_routes,
        base_path=settings.base_path or "",
        tests_per_day=2,
        expected_sleep_seconds=12 * 60 * 60,
        config=config,
    )

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
