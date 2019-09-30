from collections import OrderedDict
import logging
import configargparse
import tomlkit
from murakami.server import MurakamiServer

config = None


class TomlConfigFileParser(configargparse.ConfigFileParser):
    def get_syntax_description(self):
        msg = ("Parses a TOML-format configuration file "
               "(see https://github.com/toml-lang/toml for the spec).")
        return msg

    def parse(self, stream):
        global config
        config = tomlkit.parse(stream.read())
        settings = OrderedDict()
        for key, value in config["settings"].items():
            settings[key] = str(value)

        return settings

def main():
    parser = configargparse.ArgParser(
        auto_env_var_prefix="murakami_",
        config_file_parser_class=TomlConfigFileParser,
        default_config_files=[
            "/etc/murakami/murakami.toml",
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
    settings = parser.parse_args()

    logging.basicConfig(
        level=settings.loglevel,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s",
    )

    server = MurakamiServer(
        port=settings.port or 8080,
        hostname=settings.hostname,
        ssl_options=settings.ssl_options,
        additional_routes=settings.additional_routes,
        base_path=settings.base_path or "",
        config=config,
    )

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
