# Murakami

Murakami is a tool for creating an automated internet measurement service, running in a Docker container. A Murakami measurement container can be configured to automatically run supported tests four times a day using a randomized schedule, and export each test result to a local storage device, to one or more remote servers via SCP, or to a Google Cloud Storage bucket. Results are saved as individual files in JSON new line format (`.jsonl`).

## Supported Measurement Tests

* [M-Lab Network Diagnostic Tool](https://www.measurementlab.net/tests/ndt/) (NDT) - both [ndt5](https://www.measurementlab.net/tests/ndt/ndt5) and [ndt7](https://www.measurementlab.net/tests/ndt/ndt7) protocols, using the [libndt client library](https://github.com/measurement-kit/libndt)
* [Neubot DASH](https://github.com/neubot/dash) - Dynamic Adaptive Streaming over HTTP, hosted by M-Lab
* [speedtest-cli](https://github.com/sivel/speedtest-cli) - Command line interface for testing internet bandwidth using speedtest.net

## Murakami Deployment Scenarios

Murakami supports three types of container deployment scenarios on supported systems:

* **[Standalone](INSTALL-MURAKAMI-STANDALONE.md)**: a single Murakami device, configured on-device
* **[Local Managed](INSTALL-MURAKAMI-LOCAL-MANAGED.md)**: one or more Murakami devices in a single network, configured individually on-device, or using a [Mozilla WebThings Gateway](https://iot.mozilla.org/gateway/) on the same network, via the [M-Lab WebThings Murakami Add-on](#)
* **[Balena Cloud](INSTALL-MURAKAMI-BALENA-CLOUD.md)**: one or more Murakami devices, configured and managed by the [Balena Cloud IoT platform](https://www.balena.io)

## Supported Operating Systems

Murakami supports Linux operating systems like Ubuntu, Debian, etc. Windows is not supported. Mac OS is supportable as a standalone device, but is not completely compatible with the Webthings interface. Balena cloud has not beed tested on Mac OS.

**TO DO:** test deployment on MacOS

## Murakami Configurations and Customization

A Murkami container can be configured flexibly depending on the deployment scenario. If you simply run a Murakami container using M-Lab's pre-built images on Dockerhub, by default all tests are configured to run four times daily at randomized intervals, but no data exporters enabled. This section focuses on which options can be configured using the file `murakami.toml` OR using environment variables. Examples are provided in later sections of this document.

The Murakami container can be customized using:
* environment variables on the command line when running docker (Standalone, Local Managed)
* environment variables in a file, passed on the command line when running docker (Standalone, Local Managed)
* customizing the `murakami.toml` configuration file (Standalone, Local Managed, Balena Cloud)
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
| private_key = "/murakami/keys/id_rsa_murakami" | MURAKAMI_EXPORTERS_SCP_PRIVATE_KEY | The system path within the Murakami container where the SCP user's private SSH key is located. |
| | | | |
| [exporters.gcs] | | | The 'gcs' exporter defines a storage bucket in a Google Cloud Storage project where test data should be saved. |
| type = "gcs" | MURAKAMI_EXPORTERS_GCS_TYPE | gcs | |
| enabled = true | MURAKAMI_EXPORTERS_GCS_ENABLED | 0, 1, true, false | |
| target = "gs://murakami-gcs-test/" | MURAKAMI_EXPORTERS_GCS_TARGET | gs://bucketname | Defines the GCS storage bucket name where data should be stored. |
| service_account = "murakami-test-gcs@mlab-sandbox.iam.gserviceaccount.com" | MURAKAMI_EXPORTERS_GCS_SERVICE_ACCOUNT | The name of the GCS service account which has access to write data to the GCS storage bucket. |
| key = "/murakami/keys/murakami-gcs-serviceaccount.json" | MURAKAMI_EXPORTERS_GCS_KEY | The system path within the Murakami container where the GCS service account's JSON keyfile is located. |

Multiple exporters of any type are supported as well. For example if you wanted to define two different SCP servers or GCS storage buckets where data should be exported, the config file exporters section might look like this:

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

## M-Lab Supported Dockerhub Images and Tags

**TO DO** Describe how we structure tags for different system architectures here.
