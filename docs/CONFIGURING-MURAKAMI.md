# Configuring Murakami

A Murakami container is configured using variables that are either set when you
build or run a Murakami Docker image or by reading them from your Balena Fleet
or Device variables. The four methods of setting variables are:

* **inline** : in-line in a terminal command when you build/run the Murakami Docker container
* **text file** : included in a plain text file in a terminal command when you
  build/run the Murakami Docker container
* **.toml file** : included in a `.toml` file in a terminal command when you
  build/run the Murakami Docker container
* **Balena fleet/device variables** : All variables are set in your Balena fleet
or devices

How you set your configuration variables will depend on your personal
preferences and/or your specific deployment scenario. For Balena managed fleets,
set all variables there. For other deployment types, the include file methods
are probably most useful. You have the option to include variables in text
format or in `.toml` file format.

## Supported Configuration Variables

Below we provide a list of all possible Murakami configuration variables and
descriptions, using the inline and text file format. Please see
[murakami.toml.example](https://github.com/m-lab/murakami/blob/master/murakami.toml.example)
for using the `.toml` file format.

### Inline and Text File Format

| Variable | Options/examples | Description |
| ---------------------------------- | ---------------- | -------- |
| **Settings** | | General settings for the Murakami container. |
| MURAKAMI_SETTINGS_PORT | `80`, `8080` | Sets the web port used by the Murakami WebThing code |
| MURAKAMI_SETTINGS_WEBTHINGS | `0`, `1`, `true`, `false` | If set to `1` or `true`, the container will advertise its test runners as WebThings which can then be toggled using a Mozilla WebThings Gateway |
| MURAKAMI_SETTINGS_LOGLEVEL | `DEBUG` | Sets the log level for the Murakami service |
| MURAKAMI_SETTINGS_IMMEDIATE | `0`, `1`, `true`, `false` | If set to `1` or `true`, instructs the container to run the first set of tests when it starts. |
| MURAKAMI_SETTINGS_TESTS_PER_DAY | Integer | Recommended value is between 4-6 times per day. Murakami will divide a 24 hour period by this number, and select a randomized time within each period to run enabled tests. For example, if `6` times per day is set: `24 / 6 = 4` tests will run at a randomized time approximately every four hours. **Note: M-Lab will rate limits clients running tests to the same server from the same IP address after ~40 tests in a 24 hour period.** |
| **_Settings Metadata_** | | These three settings variables are useful for defining metadata about the connection being measured by an individual Murakami device/container. For example, `LOCATION` could be a named location, or a device id. `NETWORK_TYPE` could be the type of network, such as `egress` or `wifi`, but could also be used to designate the ISP name. **If set, these variables are used within test results filenames and as fields within each test result.** These variable names will be generalized and renamed in a future release, per [Issue #93](https://github.com/m-lab/murakami/issues/93) |
| MURAKAMI_SETTINGS_LOCATION | any string | Set location of the Murakami device. If set, value is used in exported test file names. |
| MURAKAMI_SETTINGS_NETWORK_TYPE | any string | Set the type of network where the Murakami device is running. If set, value is used in exported test file names. |
| MURAKAMI_SETTINGS_CONNECTION_TYPE | any string | Set the type of connection the Murakami device is using. If set, value is used in exported test file names |
| | |
| **Exporters** | | Exporters' variables define where test data should be saved or exported. For each exporter all variables listed must be defined. |
| **_Local Exporter_** | | The 'local' exporter defines where on the system's local disk to save test results. |
| MURAKAMI_EXPORTERS_LOCAL_TYPE | local | |
| MURAKAMI_EXPORTERS_LOCAL_ENABLED | 0, 1, true, false | |
| MURAKAMI_EXPORTERS_LOCAL_PATH | Any system path available to the Murakami container service may be used to save local data. (i.e. `/data/`) |
| | |
| **_Secure Copy Exporter (SSH/SCP)_** | | The 'scp' exporter defines a remote server where data should be copied. The server must be configured to allow secure copy via SSH using a private key file. |
| MURAKAMI_EXPORTERS_SCP_TYPE | `scp` | |
| MURAKAMI_EXPORTERS_SCP_ENABLED | `0`, `1`, `true`, `false` | |
| MURAKAMI_EXPORTERS_SCP_TARGET | `myserver.com:system/path/` | Defines the remote server and system path where the SCP exporter should save data. A server's IP address is also supported. |
| MURAKAMI_EXPORTERS_SCP_PORT | 22, alternate SCP port used by the remote server | Defines the port used by the remote server for the server's SCP/SSH service. |
| MURAKAMI_EXPORTERS_SCP_USERNAME | remote server username | Defines the username to be used by the SCP exporter. |
| MURAKAMI_EXPORTERS_SCP_KEY | The system path within the Murakami container where the SCP user's private SSH key is located. (i.e. `/murakami/configs/id_rsa_murakami` | |
| | |
| **_Google Cloud Storage (GCS) Exporter_** | | The 'gcs' exporter defines a storage bucket in a Google Cloud Storage project where test data should be saved. |
| MURAKAMI_EXPORTERS_GCS_TYPE | gcs | |
| MURAKAMI_EXPORTERS_GCS_ENABLED | 0, 1, true, false | |
| MURAKAMI_EXPORTERS_GCS_TARGET | gs://bucketname | Defines the GCS storage bucket name where data should be stored. |
| MURAKAMI_EXPORTERS_GCS_KEY | The system path within the Murakami container where the GCS service account's JSON keyfile is located. (i.e. `/murakami/configs/murakami-gcs-serviceaccount.json`) |
| | |
| **_HTTP Exporter_** | | The HTTP exporter is provided as a means of posting test results to an instance of [Murakami-Viz](https://github.com/m-lab/murakami-viz/) or other similar services. |
| MURAKAMI_EXPORTERS_HTTP0_TYPE | http | |
| MURAKAMI_EXPORTERS_HTTP0_ENABLED | 0, 1, true, false | Enables or disables the HTTP exporter |
| MURAKAMI_EXPORTERS_HTTP0_URL | "<url or IP address>/api/v1/runs" | Designated URL where you are hosting Murakami Viz, referencing the API endpoint. |
| | |
| **Enabled Tests** | | |
| MURAKAMI_TESTS_DASH_ENABLED | 0, 1, true, false | Enables or disables the DASH test runner |
| MURAKAMI_TESTS_NDT5_ENABLED | 0, 1, true, false | Enables or disables the NDT5 test runner |
| MURAKAMI_TESTS_NDT7_ENABLED | 0, 1, true, false | Enables or disables the NDT7 test runner |
| MURAKAMI_TESTS_SPEEDTESTMULTI_ENABLED | 0, 1, true, false | Enables or disables the speedtest-cli multi-stream test runner |
| MURAKAMI_TESTS_SPEEDTESTSINGLE_ENABLED | 0, 1, true, false | Enables or disables the speedtest-cli single-stream test runner |

Multiple exporters of any type are supported. For example if you wanted to
define two different SCP servers or GCS storage buckets where data should be
exported, the config file exporters section might look like this:

```
MURAKAMI_EXPORTERS_GCS1_TYPE = "gcs"
MURAKAMI_EXPORTERS_GCS1_ENABLED = "true"
MURAKAMI_EXPORTERS_GCS1_TARGET = "gs://<GCS BUCKET NAME & PATH>/"
MURAKAMI_EXPORTERS_GCS1_SERVICE_ACCOUNT = "<SERVICE ACCOUNT NAME>@<GCS_PROJECTt>.iam.gserviceaccount.com"
MURAKAMI_EXPORTERS_GCS1_KEY = "/murakami/configs/<SERVICE ACCOUNT KEY FILE>.json"

MURAKAMI_EXPORTERS_GCS2_TYPE = "gcs"
MURAKAMI_EXPORTERS_GCS2_ENABLED = "true"
MURAKAMI_EXPORTERS_GCS2_TARGET = "gs://<GCS BUCKET NAME & PATH>/"
MURAKAMI_EXPORTERS_GCS2_SERVICE_ACCOUNT = "<SERVICE ACCOUNT NAME>@<GCS_PROJECTt>.iam.gserviceaccount.com"
MURAKAMI_EXPORTERS_GCS2_KEY = "/murakami/configs/<SERVICE ACCOUNT KEY FILE>.json"
```

For complete configuration examples for each deployment type, please see:
* [Murakami Standalone Docker install](docs/INSTALL-MURAKAMI-STANDALONE.md)
* [Murakami Standalone Docker install, managed by Mozilla WebThings Gateway](docs/INSTALL-MURAKAMI-LOCAL-MANAGED.md)
* [Murakami Balena Cloud](docs/INSTALL-MURAKAMI-BALENA-CLOUD.md)
