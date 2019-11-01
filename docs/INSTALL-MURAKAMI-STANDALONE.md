# Installation and Use - Murakami Container on a Standalone Device

## Supported System Architectures for non-IoT managed Murakami Devices

For single or multiple Murakami devices running in a single network, M-Lab provides [pre-built Docker images](https://hub.docker.com/r/measurementlab/murakami) supporting the following systems:

* armv7hf
* (in testing) armv8/aarch64
* (in testing) x86
* (in testing) x64

## Setup for Standalone or WebThings Gateway Managed Murakami Measurement Devices 

### Install & Configure the Host OS

Our documentation currently focuses on armv7hf and armv8/aarch64 systems that have been tested by the M-Lab team. Below we list links to system images for ODROID brand armv7hf single board computers from Hardkernel.

* odroid-xu4 - https://wiki.odroid.com/odroid-xu4/os_images/linux/start
* odroid-c2 - https://wiki.odroid.com/odroid-c2/os_images/ubuntu/ubuntu
* odroid-c1 - https://wiki.odroid.com/odroid-c1/os_images/ubuntu/ubuntu
* odroid-n2 - https://wiki.odroid.com/odroid-n2/os_images/ubuntu

1. Install the OS onto an SD card or eMMC chip. 
2. Configure your system and get it connected to your local network. We recommend that you connect the system using ethernet for optimal measurements. However, if you wish to measure your WiFi connection, assuming the system has a WiFi card ([example](https://ameridroid.com/products/wifi-module-0)), you can use the system utility `nmtui` on the command line to connect to and save the WiFi connection.

Note that we do not provide recommendations on how you configure your host OS. However, we do recommend that you change the default `root` user and `odroid` user password(s), run `apt update && apt upgrade`, and keep your system secure by regularly updating it.

### Install Docker

You can install Docker in different ways. We tested using installation from package repositories, which worked fine.

* Install Docker.io: `apt install docker.io`
* Enable the Docker daemon to start on boot: `systemctl enable docker`
* Start the Docker daemon: `systemctl start docker`

### Run Murakami Using M-Lab Pre-built images

M-Lab provides pre-built Docker images that can be easily used to run a Murakami container using a single command. The SCP and GCS exporters require additional account and access setup. The examples below describe options for running Murakami.

#### Run Murakami Container Using the Local Storage Exporter

After getting your host OS installed and configured, and with Docker installed, decide where to store test results on the local system. After that, pull and start the container using a config file, or using environment variables. The example below assumes you are logged into your device as the root user, and have a terminal open in the folder `/root/`. 

1. First, create a folder called `data` - `$ mkdir data` to use to store test result data
2. Pull and run the Murakami Docker image for your system architecture from M-Lab's Dockerhub, mounting the folder `data` inside the container:

```
docker run --restart --network=host -e "MURAKAMI_EXPORTERS_LOCALHOST_TYPE=local" -e "MURAKAMI_EXPORTERS_LOCALHOST_ENABLED=true" -e "MURAKAMI_EXPORTERS_LOCALHOST_PATH=/data/" --volume /root/data:/data/ measurementlab/murakami:armv7-latest  --immediate
```

The example above will restart the Murakami container when the host OS's Docker service starts, so it will start when the device boots or restarts. `--network=host` instructs the container to use the host device's network settings. The flag `--immediate` instructs the Murakami daemon to run the first round of tests as soon as the container starts. Test results will be saved in `/root/data`.

The command above also starts the Murakami container in the foreground, and will show the container logs in your current console. This is great for an initial test to see what Murakami is doing. But you might want to start the Murakami container in the background and leave it running, then come back to access your data or view the Docker logs later. To do this use the `-d` flag:

```
docker run -d --restart --network=host -e "MURAKAMI_EXPORTERS_LOCALHOST_TYPE=local" -e "MURAKAMI_EXPORTERS_LOCALHOST_ENABLED=true" -e "MURAKAMI_EXPORTERS_LOCALHOST_PATH=/data/" --volume /root/data:/data/ measurementlab/murakami:armv7-latest  --immediate
```

This will print the ID of your container and return to your command prompt. It will look something like this: `27ad15bfab4b1242537147f266ee06eb9eb7658bb64d576bfb99dd4e47c53c53`. To view the running logs of that container: `docker logs --follow 27ad15bfab4b1242537147f266ee06eb9eb7658bb64d576bfb99dd4e47c53c53`. When you're done viewing logs, type `Ctrl-c`.

Optionally, you can add all your environment variables to a local file and use that in your `docker run` command instead of entering them all on the command line. For example, create a file called `env-vars` containing:

```
MURAKAMI_EXPORTERS_LOCALHOST_TYPE=local
MURAKAMI_EXPORTERS_LOCALHOST_ENABLED=true
MURAKAMI_EXPORTERS_LOCALHOST_PATH=/data/
```
Then run: `docker run --env-file env-vars --network=host --volume /root/data:/data/ measurementlab/murakami:armv7-latest --immediate`

You may also define your configuration in a `.toml` formatted file. Download a copy of [murakami.toml.example](https://github.com/m-lab/murakami/blob/master/murakami.toml.example) and customize it to your needs. In the example above, the contents would look like:

```
[settings]
port = 80
loglevel = "DEBUG"
immediate = 1
hostname = "<DEVICE HOSTNAME>"
webthings = 1
location = "<DEVICE LOCATION>"
network-type = "<TYPE OF NETWORK>"
connection-type = "<TYPE OF CONNECTION"

[exporters]

  [exporters.local]
  type = "local"
  enabled = true
  path = "/murakami/data/"

```

Save this file in a directory that will be accessible to the container (in this case, we copied ours into the `keys` folder) and then use this command to start the container:

```
docker run -d --network host --volume /root/data:/var/lib/murakami/ --volume /root/keys:/murakami/keys/ measurementlab/murakami:latest -c /murakami/keys/murakami.toml
```

#### Using the Secure Copy Protocol (SCP) and/or Google Cloud Storage Storage (GCS) Exporters

Each individual test result file can be sent to one or more remote central storage locations, using available **exporters**. Currently Murakami provides two remote storage exporters: Secure Copy Protocol (SCP) and Google Cloud Storage (GCS). Multiple exporters of both types can be used.

To add an SCP or GCS exporter, the following environment variables should be defined in a local file, or used at the command line when starting the Murakami container:

```
MURAKAMI_EXPORTERS_SCP_TYPE=scp
MURAKAMI_EXPORTERS_SCP_ENABLED=true
MURAKAMI_EXPORTERS_SCP_TARGET=<YOUR SERVER HOSTNAME OR IP ADDRESS>:<DIRECTORY TO SAVE FILES>/
MURAKAMI_EXPORTERS_SCP_PORT=22
MURAKAMI_EXPORTERS_SCP_USERNAME=<SCP USERNAME>
MURAKAMI_EXPORTERS_SCP_KEY=/murakami/keys/<NAME OF YOUR SSH PRIVATE KEY FILE>
MURAKAMI_EXPORTERS_GCS_TYPE=gcs
MURAKAMI_EXPORTERS_GCS_ENABLED=true
MURAKAMI_EXPORTERS_GCS_TARGET=gs://<YOUR GCS STORAGE BUCKET>/<BUCKET DIRECTORY>/
MURAKAMI_EXPORTERS_GCS_ACCOUNT=<YOUR GCS SERVICE ACCOUNT NAME>@<GCS PROJECT>.iam.gserviceaccount.com
MURAKAMI_EXPORTERS_GCS_KEY=/murakami/keys/<YOUR SERVICE ACCOUNT KEY>.json
```

If using a `.toml` formatted configuration file instead of environment variable format, the example above would look like:

```
[settings]
port = 80
loglevel = "DEBUG"
immediate = 1
hostname = "<DEVICE HOSTNAME>"
webthings = 1
location = "<DEVICE LOCATION>"
network-type = "<TYPE OF NETWORK>"
connection-type = "<TYPE OF CONNECTION"

[exporters]

  [exporters.local]
  type = "local"
  enabled = true
  path = "/murakami/data/"

  [exporters.scp]
  type = "scp"
  enabled = true
  target = "<YOUR SERVER HOSTNAME OR IP ADDRESS>:<DIRECTORY TO SAVE FILES>/"
  port = 22
  username = "<SCP USERNAME>"
  key = "/murakami/keys/<NAME OF YOUR SSH PRIVATE KEY FILE>"

  [exporters.gcs]
  type = "gcs"
  enabled = true
  target = "gs://<YOUR GCS STORAGE BUCKET>/<BUCKET DIRECTORY>/"
  account = "<YOUR GCS SERVICE ACCOUNT NAME>@<GCS PROJECT>.iam.gserviceaccount.com"
  key = "/murakami/keys/<YOUR SERVICE ACCOUNT KEY>.json"
```

Using the SCP and GCS exporters requires additional setup on the remote SCP server for SCP, and in your Google Cloud Storage project fof GCS:

* **SCP exporter**: requires the username which has access to login to the remote server via SSH, and that user's private SSH key. We created a unique SSH user and key for our testing.
* **GCS exporter**: requires a [Google Cloud Platform Project](https://cloud.google.com/docs/overview/), a [Storage Bucket](https://cloud.google.com/storage/docs/), and a [Service Account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) with the IAM Roles: _Storage Object Creator_, _Storage Object Viewer_, and _Storage Legacy Bucket Writer_. We reommend applying these roles for the Storage Bucket only, and not project-wide. See Google's [IAM best practice guides](https://cloud.google.com/blog/products/gcp/iam-best-practice-guides-available-now) for more information. An exported [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) is also required.

In the examples above, once the SCP and GCS account keys are created, we securely copied the keys to the computer where the Murakami container will run, in a folder called `keys`. 

Then when we run the Murakami container, we can map the `keys` folder as a volume using a file containing environment variables:

`docker run --env-file /root/env_vars --network=host --volume /root/data:/var/lib/murakami/ --volume /root/keys:/murakami/keys/ measurementlab/murakami:armv7-latest`

or using a `.toml` configuration file:

`docker run --network=host --volume /root/data:/var/lib/murakami/ --volume /root/keys:/murakami/keys/ measurementlab/murakami:armv7-latest -c /murakami/keys/murakami.toml`


#### Enabling/Disabling Individual Test Runners

By default, all availeble tests are enabled. But if desired, you can define which tests a Murakami container should run using environment variables or configuration file values.

If using environment variables:

```
MURAKAMI_TESTS_DASH_ENABLED = 0
MURAKAMI_TESTS_NDT5_ENABLED = 0
MURAKAMI_TESTS_NDT7_ENABLED = 1
MURAKAMI_TESTS_SPEEDTEST_ENABLED = 1
```

Or if using a `.toml` configuration file:

```
[tests]

  [tests.dash]
  enabled = false

  [tests.ndt5]
  enabled = false

  [tests.ndt7]
  enabled = true

  [tests.speedtest]
  enabled = true
```  
