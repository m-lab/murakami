import configargparse
import logging
from murakami.server import MurakamiServer


def main():
    parser = configargparse.ArgParser(
        description="The Murakami network test runner.")
    parser.add(
        "-p",
        "--port",
        type=int,
        default=80,
        env_var="MURAKAMI_PORT",
        help="The port to listen on for incoming connections (default: 80).",
    )
    parser.add(
        "-n",
        "--hostname",
        nargs="?",
        env_var="MURAKAMI_HOSTNAME",
        help="The mDNS hostname for WebThings (default: automatic).",
    )
    parser.add(
        "-s",
        "--ssl-options",
        nargs="?",
        dest="ssl_options",
        env_var="MURAKAMI_SSL_OPTIONS",
        help="SSL options for the WebThings server (default: none).",
    )
    parser.add(
        "-r",
        "--additional-routes",
        nargs="?",
        dest="additional_routes",
        env_var="MURAKAMI_ADDITIONAL_ROUTES",
        help=
        "List of additional routes for the WebThings server (default: none).",
    )
    parser.add(
        "-b",
        "--base-path",
        default="",
        dest="base_path",
        env_var="MURAKAMI_BASE_PATH",
        help="Base URL path to use, rather than '/' (default: '').",
    )
    parser.add(
        "-l",
        "--log",
        dest="loglevel",
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        env_var="MURAKAMI_LOGLEVEL",
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
        base_path=settings.base_path or '',
    )

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
