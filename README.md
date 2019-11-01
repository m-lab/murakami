# Murakami

Murakami is a tool for creating an automated internet measurement service, running in a Docker container. A Murakami measurement container will automatically run supported tests four times a day using a randomized schedule, and can be configured to export each test result to a local storage device, to one or more remote servers via SCP, or to a Google Cloud Storage bucket. Results are saved as individual files in JSON new line format (`.jsonl`).

## What Does the Name Mean?

**What do we talk about when we talk about running tests?** The M-Lab team talks about this a lot, so it's no wonder that the name "Murakami" pays homage to the renown author Haruki Murakami, who's book [_What I Talk About When I Talk About Running_](http://www.harukimurakami.com/book/what-i-talk-about-when-i-talk-about-running-a-memoir) provided us inspiration.

## Contributing to Murakami

Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Supported Measurement Tests

* [M-Lab Network Diagnostic Tool](https://www.measurementlab.net/tests/ndt/) (NDT) using the [libndt client library](https://github.com/measurement-kit/libndt)
  * [ndt5 protocol](https://www.measurementlab.net/tests/ndt/ndt5)
  * [ndt7 protocol](https://www.measurementlab.net/tests/ndt/ndt7)
* [Neubot DASH](https://github.com/neubot/dash) - Dynamic Adaptive Streaming over HTTP, hosted by M-Lab
* [speedtest-cli](https://github.com/sivel/speedtest-cli) - Command line interface for testing internet bandwidth using speedtest.net

## Murakami Deployment Scenarios

Murakami supports three types of Docker container deployments on supported systems:

* **[Standalone](INSTALL-MURAKAMI-STANDALONE.md)**: a single Murakami device, configured on-device
* **[Standalone Locally Managed](INSTALL-MURAKAMI-LOCAL-MANAGED.md)**: one or more Murakami devices in a single network, configured individually on-device, or using a [Mozilla WebThings Gateway](https://iot.mozilla.org/gateway/) on the same network
* **[Fleet Managed Murakami using Balena Cloud](INSTALL-MURAKAMI-BALENA-CLOUD.md)**: one or more Murakami devices, configured and managed by the [Balena Cloud IoT platform](https://www.balena.io)

It is also possible to install Murakami directly on supported systems without Docker, however currently documenting direct system installation of Murakami is beyond our project scope. Future testing and documentation is needed to test and confirm supported systems and requirements.

## Supported Operating Systems

Murakami supports Linux operating systems like Ubuntu, Debian, etc. Windows is not supported. Mac OS may work, but is yet untested.

## Murakami Configurations and Customization

A Murkami container can be configured flexibly depending on the deployment scenario. If you simply run a Murakami container using M-Lab's pre-built images on Dockerhub, by default all tests are configured to run four times daily at randomized intervals, but with no data exporters enabled. This section focuses on which options can be configured using the file `murakami.toml` OR using environment variables.

The Murakami container can be customized using:
* environment variables on the command line when running docker (Standalone, Standalone Locally Managed)
* environment variables in a file, passed on the command line when running docker (Standalone, Standalone Locally Managed)
* customizing the `murakami.toml` configuration file (Standalone, Standalone Locally Managed)
* environment variables in your Balena Cloud project, or per device (Balena Cloud)

The table below summarizes the options you can configure in `murakami.toml` and how to format the options as command line variables at the command line.

| murakami.toml | corresponding environment variable | options/examples | function |
| ------------- | ---------------------------------- | ---------------- | -------- |
| [settings] | | |
| port = 80  | MURAKAMI_SETTINGS_PORT | 80, 8080 | Sets the web port used by the Murakami WebThing code |
| loglevel = "DEBUG" | MURAKAMI_SETTINGS_LOGLEVEL | DEBUG, ?, ? | Sets the log level for the Murakami service |
| immediate = 1 | MURAKAMI_SETTINGS_IMMEDIATE | 0, 1, true, false | If set to `1` or `true`, instructs the container to run the first set of tests when it starts |
| location = "Baltimore" | MURAKAMI_SETTINGS_LOCATION | any string | Optional - If set, value is used in exported test file names. |
| network_type = "home" | MURAKAMI_SETTINGS_NETWORK_TYPE | any string | Optional - If set, value is used in exported test file names |
| connection_type = "wired" | MURAKAMI_SETTINGS_CONNECTION_TYPE | any string | Optional - If set, value is used in exported test file names |
| [exporters] | | The 'exporters' configuration sections OR environment variables define where test data should be saved or exported. For each exporter all variables listed must be defined. |
| | | | |
| [exporters.local] | | | The 'local' exporter defines where on the system's local disk to save test results. |
| type = "local" | MURAKAMI_EXPORTERS_LOCAL_TYPE | local | | |
| enabled = true | MURAKAMI_EXPORTERS_LOCAL_ENABLED | 0, 1, true, false | |
| path = "/data/" | MURAKAMI_EXPORTERS_LOCAL_PATH | Any system path available to the Murakami container service may be used to save local data. |
| | | | |
| [exporters.scp] | | | The 'scp' exporter defines a remote server where data should be copied. The server must be configured to allow secure copy via SSH using a private key file. |
| type = "scp" | MURAKAMI_EXPORTERS_SCP_TYPE | scp | |
| enabled = true | MURAKAMI_EXPORTERS_SCP_ENABLED | 0, 1, true, false | |
| target = "myserver.com:system/path/" | MURAKAMI_EXPORTERS_SCP_TARGET | hostname:path/ | Defines the remote server and system path where the SCP exporter should save data. A server's IP address is also supported. |
| port = 22 | MURAKAMI_EXPORTERS_SCP_PORT | 22, alternate SCP port used by the remote server | Defines the port used by the remote server for the server's SCP/SSH service. |
| username = "murakami" | MURAKAMI_EXPORTERS_SCP_USERNAME | remote server username | Defines the username to be used by the SCP exporter. |
| key = "/murakami/keys/id_rsa_murakami" | MURAKAMI_EXPORTERS_SCP_KEY | The system path within the Murakami container where the SCP user's private SSH key is located. |
| | | | |
| [exporters.gcs] | | | The 'gcs' exporter defines a storage bucket in a Google Cloud Storage project where test data should be saved. |
| type = "gcs" | MURAKAMI_EXPORTERS_GCS_TYPE | gcs | |
| enabled = true | MURAKAMI_EXPORTERS_GCS_ENABLED | 0, 1, true, false | |
| target = "gs://murakami-gcs-test/" | MURAKAMI_EXPORTERS_GCS_TARGET | gs://bucketname | Defines the GCS storage bucket name where data should be stored. |
| account = "murakami-test-gcs@mlab-sandbox.iam.gserviceaccount.com" | MURAKAMI_EXPORTERS_GCS_ACCOUNT | The name of the GCS service account which has access to write data to the GCS storage bucket. |
| key = "/murakami/keys/murakami-gcs-serviceaccount.json" | MURAKAMI_EXPORTERS_GCS_KEY | The system path within the Murakami container where the GCS service account's JSON keyfile is located. |

Multiple exporters of any type are supported. For example if you wanted to define two different SCP servers or GCS storage buckets where data should be exported, the config file exporters section might look like this:

```
[exporters]

  [exporters.gcs1]
  type = "gcs"
  enabled = true
  target = "gs://murakami-storage-bucket-archive/"
  service_account = "murakami-test-gcs@mlab-sandbox.iam.gserviceaccount.com"
  key = "/murakami/keys/murakami-gcs-serviceaccount.json"

  [exporters.gcs2]
  type = "gcs"
  enabled = true
  target = "gs://murakami-storage-bucket-access/"
  service_account = "murakami-test-gcs@mlab-sandbox.iam.gserviceaccount.com"
  key = "/murakami/keys/murakami-gcs-serviceaccount.json"
```
OR as environment variables:
```
MURAKAMI_EXPORTERS_GCS1_TYPE = "gcs"
MURAKAMI_EXPORTERS_GCS1_ENABLED = "true"
MURAKAMI_EXPORTERS_GCS1_TARGET = "gs://murakami-storage-bucket-archive/"
MURAKAMI_EXPORTERS_GCS1_SERVICE_ACCOUNT = "murakami-test-gcs@mlab-sandbox.iam.gserviceaccount.com"
MURAKAMI_EXPORTERS_GCS1_KEY = "/murakami/keys/murakami-gcs-serviceaccount.json"

MURAKAMI_EXPORTERS_GCS2_TYPE = "gcs"
MURAKAMI_EXPORTERS_GCS2_ENABLED = "true"
MURAKAMI_EXPORTERS_GCS2_TARGET = "gs://murakami-storage-bucket-access/"
MURAKAMI_EXPORTERS_GCS2_SERVICE_ACCOUNT = "murakami-test-gcs@mlab-sandbox.iam.gserviceaccount.com"
MURAKAMI_EXPORTERS_GCS2_KEY = "/murakami/keys/murakami-gcs-serviceaccount.json"
```

For complete configuration examples for each deployment type, please see:
* [Murakami Standalone Docker install](docs/INSTALL-MURAKAMI-STANDALONE.md)
* [Murakami Standalone Docker install, managed by Mozilla WebThings Gateway](docs/INSTALL-MURAKAMI-LOCAL-MANAGED.md)
* [Murakami Balena Cloud](docs/INSTALL-MURAKAMI-BALENA-CLOUD.md)

## M-Lab Supported Dockerhub Images and Tags

Measurement Lab published supported, pre-built Docker container images on Dockerhub. As new system architectures are tested, we publish images using the pattern: `measurementlab/murakami-<SYSTEM ARCHITECTURE>:<TAG>`

Tags are either a release number or "latest". 

For example, the "latest" image for the armv7 architecture would be: `measurementlab/murakami-armv7:latest`
Or we could refernece a release tag: `measurementlab/murakami-armv7:v2.0`

Please visit [our repo on Dockerhub](https://cloud.docker.com/repository/docker/measurementlab/murakami/general) for a complete list of images/tags.

## Building Murakami Images

If you are interested in building your own Murakami Docker images, please see our [BUILD instructions](docs/BUILD.md).
