# Installation and Use - Murakami Container on a Standalone Device

## Supported System Architectures for non-IoT managed Murakami Devices

For single or multiple Murakami devices running in a single network, M-Lab provides [pre-built Docker images](https://hub.docker.com/r/measurementlab/murakami) supporting the following systems:

* armv7hf
* (in testing) armv8/aarch64
* (in testing) x86
* (in testing) x64 (need to test)

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

**TO DO** Provide minimual instructions on installing Docker.

* Enable the Docker daemon to start on boot.

### Run Murakami Using M-Lab Pre-built images

M-Lab provides pre-built Docker images that can be easily used to run a Murakami container using a single command. The SCP and GCS exporters require additional account and access setup. The examples below describe options for running Murakami.

#### Run Murakami Container Using the Local Storage Exporter

After getting your host OS installed and configured, and with Docker installed, decide where to store test results on the local system. After that, pull and start the container using a config file, or using environment variables. The example below assume you are logged into your device as a user named `murakami`, have a terminal open in the folder `/home/murakami`. 

1. First, create a folder called `data` - `$ mkdir data` to use to store test result data
2. Pull and run the Murakami Docker image for your system architecture from M-Lab's Dockerhub, mounting the folder `data` inside the container:

```
docker run --restart -e "MURAKAMI_EXPORTERS_LOCALHOST_TYPE=local" -e "MURAKAMI_EXPORTERS_LOCALHOST_ENABLED=true" -e "MURAKAMI_EXPORTERS_LOCALHOST_PATH=/data/" --volume /root/data:/data/ measurementlab/murakami:armv7-latest  --immediate
```

The example above will start the Murakami container when the host OS's Docker service starts, so it will start when the device boots or restarts. The flag `--immediate` instructs the Murakami daemon to run the first round of tests as soon as the container starts. Test results will be saved in `/root/data`.

**TO DO** Test the alternative below:

Optionally, you can create a file containing all your environment variables instead of entering them all on the command line. For example, create a file called `env-vars` containing:

```
MURAKAMI_EXPORTERS_LOCALHOST_TYPE=local
MURAKAMI_EXPORTERS_LOCALHOST_ENABLED=true
MURAKAMI_EXPORTERS_LOCALHOST_PATH=/data/
```
Then run: `docker run -e env-vars --volume /root/data:/data/ measurementlab/murakami:armv7-latest --immediate`

**TO DO** Test the alternative below:

Optionally, if you prefer to use `.toml` format, you can pass a `.toml` file containing your desired configuration. For example, edit your `murkami.toml` file to include:

```
[settings]
port = 80
loglevel = "DEBUG"
immediate = 1

[exporters]

  [exporters.local]
  type = "local"
  enabled = true
  path = "/data/"
```
Then run: `docker run -c murakami.toml --volume /root/data:/data/ measurementlab/murakami:armv7-latest`

#### Using the Secure Copy Protocol (SCP) and/or Google Cloud Storage Storage (GCS) Exporters

**TO DO**

#### Enabling/Disabling Individual Test Runners

**TO DO**
