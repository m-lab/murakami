# Configuring Murakami

A Murakami container is configured using variables. You can set or include
configuration variables when you build or run a Murakami Docker image or by they
can be set within a Balena Fleet or Device when using Balena Cloud. These
methods of setting variables have been tested and are supported:

* **in-line** : in-line in a terminal command when you build/run the Murakami
  Docker container
* **included** : included as a plain text or `.toml` file when you build run
  the Murakami Docker container
* **Balena fleet/device variables** : All variables are set in your Balena fleet
  or devices

How you set your configuration variables will depend on your personal
preferences and/or your specific deployment scenario. For Balena managed fleets,
set all variables there. For other deployment types, the in-line or include file methods
are probably most useful. You have the option to include variables in text
format or in `.toml` file format.

## Supported Configuration Variables

Supported Murakami configuration variables are documented in two example
configuration files. See `configs/murakami.toml.example` for variables and
descriptions in the `.toml` file format, and `murakami.config.example` for
variables only in plain text format.

## Additional Configuration File for NDT Custom Runners

The `ndt5custom` or `ndt7custom` test runners allow you to run multiple tests
per Murakami run, use self-deployed (non-M-Lab servers) as well as M-Lab ones,
and leverage the M-Lab Locate Service to test to servers in different countries
or regions. An additional configuration file containing your list of servers is
required. You can review and customize the file
`configs/ndt-custom-config.json.example` as a starting point. See also the
section on [NDT 5 / 7 Custom Runners](SUPPORTED-TEST-RUNNERS.md) in SUPPORTED-TEST-RUNNERS.md.

## Deployment Examples

For complete configuration examples for each deployment type, please see:
* [Murakami Standalone Docker install](INSTALL-MURAKAMI-STANDALONE.md)
* [Murakami Standalone Docker install, managed by Mozilla WebThings Gateway](INSTALL-MURAKAMI-LOCAL-MANAGED.md)
* [Murakami Balena Cloud](INSTALL-MURAKAMI-BALENA-CLOUD.md)
