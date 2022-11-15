# Murakami

Murakami is a tool for creating an automated Internet measurement service,
running in a Docker container. A Murakami measurement container will
automatically run supported tests using a randomized schedule a configurable
number of times a day, and can be configured to export each test result to a
local storage device, to one or more remote servers via SCP, or to a Google
Cloud Storage bucket. Results are saved as individual files in JSON new line
format (`.jsonl`).

## Contributing to Murakami

M-Lab welcomes your contribution to Murakami development. We recommend forking
the repository and submitting pull requests to address
[issues](https://github.com/m-lab/murakami/issues) we've identified. If there is
a feature you would like to contribute that isn't in our list of issues, please
create an issue so that it can be discussed and integrated into our roadmap.

## Supported Measurement Tests

* [Network Diagnostic Tool](https://www.measurementlab.net/tests/ndt/) (NDT) -
  NDT is diagnostic and single stream performance test, originally developed by
  Internet2, and is now maintained by M-Lab. The supported NDT protocol versions
  listed below measure a connection using [different TCP congestion control
  algorithms, and have different port/firewall requirements](https://www.measurementlab.net/blog/evolution-of-ndt/#timeline).
  * [ndt5-client-go](https://www.github.com/m-lab/ndt5-client-go) - The [ndt5
    protocol](https://www.measurementlab.net/tests/ndt/ndt5/) test uses CUBIC
    TCP congestion control, and is backward compatible with previous iterations
    of the NDT server. ndt5 requires some non-standard ports to be open.
  * [ndt7-client-go](https://www.github.com/m-lab/ndt7-client-go) - The [ndt7
    protocol](https://www.measurementlab.net/tests/ndt/ndt7/) test uses BBR TCP
    congestion control for the download measurement and for upload uses the
    congestion control enabled in the client network. ndt7 uses standard ports 80/443.
* [Neubot DASH](https://github.com/neubot/dash) - Dynamic Adaptive Streaming
  over HTTP, hosted by M-Lab. [DASH](https://www.measurementlab.net/tests/neubot/) is designed to measure the quality of tested networks by emulating a video streaming player.
* [Ookla's speedtest-cli](https://www.speedtest.net/apps/cli) - Ookla's official
  command line test for testing internet bandwidth using the speedtest.net platform.
  * Both multi-stream and single-stream tests are supported
* [OONI Probe](https://ooni.org/install/cli) - The Open
  [Observatory of Network Interference](https://ooni.org) (OONI) is a non-profit free software
  project that aims to empower decentralized efforts in documenting Internet
  censorship around the world. Collect data that can potentially serve as evidence of Internet censorship since it shows how, when, where, and by whom it is implemented.

For more information about each supported test see: [Supported Tests
Runners](docs/SUPPORTED-TEST-RUNNERS.md).

To add new internet measurement tools to Murakami, see: [Adding New Measurement Tools to Murakami](docs/ADDING-NEW-TEST-RUNNERS.md)

## Supported Operating Systems

Murakami supports Linux operating systems like Ubuntu, Debian, etc. Windows is
not supported. Mac OS may work, but is yet untested.

## Configuring Murakami

A Murakami container can be configured flexibly depending on the deployment
scenario. If you simply run a Murakami container using M-Lab's `latest` [image
on Dockerhub](https://hub.docker.com/r/measurementlab/murakami/), by default all
tests are configured to run four times daily at randomized intervals, but with
no data exporters enabled. To use Murakami and save test results, either using
an individual device or a fleet of managed devices, you'll use one of the
options below to configure the container at runtime, or build your own local
container image.

The Murakami container can be configured/customized using:
* in-line environment variables on the command line when running the Docker container
* customizing the `configs/murakami.config.example` configuration file and
  passing the variables it contains on the command line when running the
  Docker container
* customizing the `configs/murakami.toml.example` configuration file and including it in a
  deployed Docker container
* environment variables in a [Balena Cloud](https://www.balena.io/cloud) fleet
  and/or per device

See [CONFIGURING-MURAKAMI](docs/CONFIGURING-MURAKAMI.md) for more information on
all configuration variables, and in our documentation specific to each deployment scenario.

## Deployment Scenarios

Murakami supports two types of Docker container deployments on supported systems:

* **[Standalone](docs/INSTALL-MURAKAMI-STANDALONE.md)**: a single Murakami device, configured on-device
* **[Fleet Managed Murakami using Balena Cloud](docs/INSTALL-MURAKAMI-BALENA-CLOUD.md)**: one or more Murakami devices, configured and managed by the [Balena Cloud IoT platform](https://www.balena.io)

It is also possible to install Murakami directly on supported systems without
Docker, however currently documenting direct system installation of Murakami is
beyond our project scope. Future testing and documentation is needed to test and
confirm supported systems and requirements.

## Dockerhub Images and Tags

Measurement Lab publishes a pre-built Murakami Docker container image
on Dockerhub tagged `latest`. Please visit [our repo on
Dockerhub](hhttps://hub.docker.com/r/measurementlab/murakami) for more details.

## Building Murakami Images

If you are interested in building your own Murakami Docker images, please see
our [BUILD instructions](docs/BUILD.md).

## Updating Your Murakami Images/Installations

Murakami is periodically updated with new measurements and features, as well as
updates to existing measurement services. M-Lab recommends keeping your Murakami installations or
container images up to date with changes in the main branch of this repository,
or with the `latest` image on Dockerhub. See the appropriate section on
_Updating Murakami_ in the supported _Deployment Scenarios_ documents
linked above for more information.

## Included Utility Scripts for Google Cloud and Balena Cloud Tasks

Utility scripts that provide some automation to setup Google Cloud resources and
provisioning new devices for a Balena Cloud fleet are available in `utilities/`.
These are designed to support M-Lab demo fleets, so please inspect and customize
them to your liking.

* `setup_bq.sh` - Intended to be run once to setup GCP resources for a new
  measurement program or demo. The Google Cloud SDK must be installed and
  authorized with an account that has IAM permissions to create GCS buckets
  and BigQuery datasets, tables and views.
* `setup_balena_device.sh` - This script can be used to provision new Murakami devices in
  your Balena Cloud fleet. It requires the balena-cli to be installed and
  authorized.
* `bq_load_murakami.sh` - Intended to be scheduled daily using scheduled jobs or
  cron, this script will load murakami test results files within a GCS bucket
  from the previous day into BigQuery tables.

For more details, see [Murakami on Google Cloud Demo](docs/GCLOUD-DEMO.md).

## Optional Prototype Data Visualization Service

An optional data visualization service,
[Murakami-Viz](https://github.com/m-lab/murakami-viz/), can be used to receive
test results from Murakami measurement devices if desired. Please see
[USING-MURAKAMI-VIZ](docs/USING_MURAKAMI_VIZ.md) for more information.

### Included Convenience Scripts

Two convenience utilities are provided with Murakami:

* [murakami_convert](docs/CONVERT-DATA.py) `scripts/convert.py`
  * A script to convert `jsonl` test results to CSV.
* [murakami_upload](docs/UPLOAD-UTILITY.py) `scripts/upload.py`
  * A script to upload previously collected test results to a newly deployed
    instance of Murakami-Viz.

## What Does the Name Mean?

**What do we talk about when we talk about running tests?** The M-Lab team talks
about this a lot, and the name "Murakami" pays homage to the renown author
Haruki Murakami, who's book [_What I Talk About When I Talk About
Running_](http://www.harukimurakami.com/book/what-i-talk-about-when-i-talk-about-running-a-memoir)
provided us inspiration.

## Acknowledgements

M-Lab would like to thank the Institute for Museum and Library Services (IMLS),
and Simmons University, whose partnership on IMLS Award
[#LG-71-18-0110-18](https://www.imls.gov/grants/awarded/lg-71-18-0110-18)
supported the development of many current Murakami features, as well as
Murakami-Viz.
