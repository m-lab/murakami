# How to run tests

This is a step by step guide for how to run tests using Murakami.

## Install Murakami

Follow the instructions [here](README.md#murakami-deployment-scenarios) to choose your method of installing Murakami.

## Set up configuration

### Using a config file

The supplied `murakami.toml` file (linked [here](murakami.toml)) offers a minimal configuration. You may use this file to customize your build with all the options (shown here)[README.md#murakami-configurations-and-customization].

Additionally, further examples of how a user may want to configure their Murakami device are shown in the `murakami.toml.example` file, linked [here](murakami.toml.example).

### With command line arguments

A number of additional and overlapping command line arguments may be added when running Murakami to customize the build. Run `murakami -h` or `murakami --help` to see the full list, which includes:

```
-c CONFIG, --config CONFIG
                        Configuration file path (default:
                        /etc/murakami/murakami.toml).
  -d DYNAMIC, --dynamic-state DYNAMIC
                        Path to dynamic configuration store, used to override
                        settings via Webthings (default:
                        /var/lib/murakami/config.json). [env var:
                        MURAKAMI_SETTINGS_DYNAMIC_STATE]
  -p PORT, --port PORT  The port to listen on for incoming connections
                        (default: 80). [env var: MURAKAMI_SETTINGS_PORT]
  -n HOSTNAME, --hostname HOSTNAME
                        The mDNS hostname for WebThings (default: automatic).
                        [env var: MURAKAMI_SETTINGS_HOSTNAME]
  -s [SSL_OPTIONS], --ssl-options [SSL_OPTIONS]
                        SSL options for the WebThings server (default: none).
                        [env var: MURAKAMI_SETTINGS_SSL_OPTIONS]
  -r [ADDITIONAL_ROUTES], --additional-routes [ADDITIONAL_ROUTES]
                        Additional routes for the WebThings server (default:
                        none). [env var: MURAKAMI_SETTINGS_ADDITIONAL_ROUTES]
  -b BASE_PATH, --base-path BASE_PATH
                        Base URL path to use, rather than '/' (default: '').
                        [env var: MURAKAMI_SETTINGS_BASE_PATH]
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level [env var: MURAKAMI_SETTINGS_LOG]
  -t TESTS_PER_DAY, --tests-per-day TESTS_PER_DAY
                        Set the number of tests per day. [env var:
                        MURAKAMI_SETTINGS_TESTS_PER_DAY]
  -i, --immediate       Immediately run available tests on startup. [env var:
                        MURAKAMI_SETTINGS_IMMEDIATE]
  -w, --webthings       Enable webthings support. [env var:
                        MURAKAMI_SETTINGS_WEBTHINGS]
  --location LOCATION   Physical place Murakami node is located (default: '').
                        [env var: MURAKAMI_SETTINGS_LOCATION]
  --network-type NETWORK_TYPE
                        Site associated with this Murakami node (default: '').
                        [env var: MURAKAMI_SETTINGS_NETWORK_TYPE]
  --connection-type CONNECTION_TYPE
                        Connection this associated with this node (default:
                        ''). [env var: MURAKAMI_SETTINGS_CONNECTION_TYPE]
```

## Start tests

How to run tests depends on your environment.

### Command line

To run Murakami straight from the command line without a Docker container:
```
poetry run murakami
```

**Note: The first time you run Murakami this way, make sure to run `poetry install` first to install all your dependencies.**

### Docker

M-Lab provides pre-built Docker images that can be easily used to run a Murakami container using a single command. All of them can be found [here](INSTALL-MURAKAMI-STANDALONE.md#run-murakami-using-m-lab-pre-built-images).

In short, the base command to run in Docker from the directory is:
```
docker run murakami
```
