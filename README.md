# Murakami

Murakami is a tool for creating an automated Internet measurement service, running in a Docker container. A Murakami measurement container will automatically run supported tests four times a day using a randomized schedule, and can be configured to export each test result to a local storage device, to one or more remote servers via SCP, or to a Google Cloud Storage bucket. Results are saved as individual files in JSON new line format (`.jsonl`).

## Contributing to Murakami

Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Supported Measurement Tests

* [Network Diagnostic Tool](https://www.measurementlab.net/tests/ndt/) (NDT) - A
  diagnostic and single stream performance test.
  * [ndt5-client-go](https://www.github.com/m-lab/ndt5-client-go)
  * [ndt7-client-go](https://www.github.com/m-lab/ndt7-client-go)
* [Neubot DASH](https://github.com/neubot/dash) - Dynamic Adaptive Streaming over HTTP, hosted by M-Lab
* [speedtest-cli](https://github.com/sivel/speedtest-cli) - A community-developed command line test for testing internet bandwidth using speedtest.net (OOKLA).
  * Both multi-stream and single-stream tests are supported

For more information about each supported test see: [Supported Tests Runners](docs/SUPPORTED-TEST-RUNNERS.md).

## Supported Operating Systems

Murakami supports Linux operating systems like Ubuntu, Debian, etc. Windows is
not supported. Mac OS may work, but is yet untested.

## Configurating Murakami

A Murakami container can be configured flexibly depending on the deployment
scenario. If you simply run a Murakami container using M-Lab's `latest` [image
on Dockerhub](https://hub.docker.com/r/measurementlab/murakami/tags?page=1&ordering=last_updated),
by default all tests are configured to run four times daily at randomized
intervals, but with no data exporters enabled. To use Murakami and save test
results, either using an individual device or a fleet of managed devices, you'll
use one of the options below to configure the container at runtime, or build
your own local container image.

The Murakami container can be configured/customized using:
* environment variables on the command line when running Docker (Standalone, Standalone Locally Managed)
* environment variables in a file, passed on the command line when running Docker (Standalone, Standalone Locally Managed)
* customizing the `murakami.toml` configuration file (Standalone, Standalone Locally Managed)
* environment variables in your Balena Cloud project, or per device (Fleet
  Managed in Balena Cloud)

See [CONFIGURING-MURAKAMI](docs/CONFIGURING-MURAKAMI.md) for more information on all configuration
variables, and in our documentation specific to each deployment scenario.

## Deployment Scenarios

Murakami supports three types of Docker container deployments on supported systems:

* **[Standalone](docs/INSTALL-MURAKAMI-STANDALONE.md)**: a single Murakami device, configured on-device
* **[Fleet Managed Murakami using Balena Cloud](docs/INSTALL-MURAKAMI-BALENA-CLOUD.md)**: one or more Murakami devices, configured and managed by the [Balena Cloud IoT platform](https://www.balena.io)

* **[Standalone Locally Managed](docs/INSTALL-MURAKAMI-LOCAL-MANAGED.md)**: Experimental support for managing Murakami test runners using a [Mozilla WebThings Gateway](https://iot.mozilla.org/gateway/) on the same network is also possible.

It is also possible to install Murakami directly on supported systems without Docker, however currently documenting direct system installation of Murakami is beyond our project scope. Future testing and documentation is needed to test and confirm supported systems and requirements.

## Dockerhub Images and Tags

Measurement Lab publishes a `latest` pre-built Murakami Docker container image
on Dockerhub. Please visit [our repo on
Dockerhub](https://cloud.docker.com/repository/docker/measurementlab/murakami/general)
for more details.

## Building Murakami Images

If you are interested in building your own Murakami Docker images, please see
our [BUILD instructions](docs/BUILD.md).

## Included Utility Scripts for Google Cloud and Balena Cloud Tasks

Utility scripts that provide some automation to setup Google Cloud resources and
provisioning new devices for a Balena Cloud fleet are available in `utilities/`.
These are designed to support M-Lab demo fleets, so please inspect and customize
them to your liking.

* `setup_bq.sh` - Intended to be run once to setup GCP resources for a new
  measurement program or demo. The Google Cloud SDK must be installed and
  authorized with an account that has IAM permissions to create GCS buckets
  and BigQuery datasets, tables and views.
* `bq_load_murakami.sh` - Intended to be scheduled daily using scheduled jobs or
  cron, this script will load murakami test results files within a GCS bucket
  from the previous day into BigQuery tables.
* `setup_balena_device.sh` - This script can be used to provision new Murakami devices in
  your Balena Cloud fleet. It requires the balena-cli to be installed and
  authorized.

## Included Convenience Scripts for Post-installation Tasks

Two convenience utilities are provided with Murakami:

* [murakami_convert](docs/CONVERT-DATA.py) `scripts/convert.py`
* [murakami_upload](docs/UPLOAD-UTILITY.py) `scripts/upload.py`

## Optional Prototype Data Visualization Service

An optional data visualization service, [Murakami-Viz](https://github.com/m-lab/murakami-viz/), can be used to receive test results from Murakami measurement devices if desired. Please see [USING-MURAKAMI-VIZ](docs/USING_MURAKAMI_VIZ.md) for more information.

## What Does the Name Mean?

**What do we talk about when we talk about running tests?** The M-Lab team talks about this a lot, so it's no wonder that the name "Murakami" pays homage to the renown author Haruki Murakami, who's book [_What I Talk About When I Talk About Running_](http://www.harukimurakami.com/book/what-i-talk-about-when-i-talk-about-running-a-memoir) provided us inspiration.

## Acknowledgements

M-Lab would like to thank the Institute for Museum and Library Services (IMLS), and Simmons University, whose partnership on IMLS Award [#LG-71-18-0110-18](https://www.imls.gov/grants/awarded/lg-71-18-0110-18) supported the development of many current Murakami features, as well as Murakami-Viz.
