# Installation and Use - Murakami Container on a Standalone Device

Murakami can be run in a Docker container on any host that supports Docker. Note
that some tests may include features that may not work on some host systems.

Standalone containers are built using the `Dockerfile` in the main directory of
this repository.

## Supported System Architectures for non-IoT managed Murakami Devices

For single or multiple Murakami devices running in a single network, M-Lab
provides [pre-built Docker
images](https://hub.docker.com/r/measurementlab/murakami) which as been tested
on the following systems:

* armv7hf
* armv8/aarch64
* x86
* x64

## Setup for Standalone or WebThings Gateway Managed Murakami Measurement Devices 

### Install & Configure the Host OS

Our documentation currently focuses on armv7hf and armv8/aarch64 systems that
have been tested by the M-Lab team. Below we list links to system images for
ODROID brand armv7hf single board computers from Hardkernel.

* odroid-xu4 - https://wiki.odroid.com/odroid-xu4/os_images/linux/start
* odroid-c2 - https://wiki.odroid.com/odroid-c2/os_images/ubuntu/ubuntu
* odroid-c1 - https://wiki.odroid.com/odroid-c1/os_images/ubuntu/ubuntu
* odroid-n2 - https://wiki.odroid.com/odroid-n2/os_images/ubuntu

1. Install the OS onto an SD card or eMMC chip. 
2. Configure your system and get it connected to your local network. We
   recommend that you connect the system using ethernet for optimal
   measurements. However, if you wish to measure your WiFi connection, assuming
   the system has a WiFi card
   ([example](https://ameridroid.com/products/wifi-module-0)), you can use the
   system utility `nmtui` on the command line to connect to and save the WiFi
   connection.

Note that we do not provide recommendations on how you configure your host OS.
However, we do recommend that you change the default `root` user and `odroid`
user password(s), run `apt update && apt upgrade`, and keep your system secure
by regularly updating it.

### Install Docker

You can install Docker in different ways. We tested using installation from
package repositories, which worked fine.

* Install Docker.io: `apt install docker.io`
* Enable the Docker daemon to start on boot: `systemctl enable docker`
* Start the Docker daemon: `systemctl start docker`

### Run Murakami Using M-Lab Pre-built images

M-Lab provides pre-built Docker images that can be easily used to run a Murakami
container using a single command. The SCP and GCS exporters require additional
account and access setup. The examples below describe options for running
Murakami.

#### Run Murakami Container Using the Local Storage Exporter

After getting your host OS installed and configured, and with Docker installed,
decide where to store test results on the local system. After that, pull and
start the container using a config file, or using environment variables. The
example below assumes you are logged into your device as the root user, and have
a terminal open in the folder `/root/`. 

1. First, create a folder called `data` - `$ mkdir data` to use to store test result data
2. Pull and run the Murakami Docker image for your system architecture from
   M-Lab's Dockerhub, mounting the folder `data` inside the container:

```
docker run --restart --network=host -e "MURAKAMI_EXPORTERS_LOCAL_TYPE=local" -e "MURAKAMI_EXPORTERS_LOCAL_ENABLED=true" -e "MURAKAMI_EXPORTERS_LOCAL_PATH=/data/" --volume /root/data:/data/ measurementlab/murakami:latest  --immediate
```

The example above will restart the Murakami container when the host OS's Docker
service starts, so it will start when the device boots or restarts.
`--network=host` instructs the container to use the host device's network
settings. The flag `--immediate` instructs the Murakami daemon to run the first
round of tests as soon as the container starts. Test results will be saved in
`/root/data`.

The command above also starts the Murakami container in the foreground, and will
show the container logs in your current console. This is great for an initial
test to see what Murakami is doing. But you might want to start the Murakami
container in the background and leave it running, then come back to access your
data or view the Docker logs later. To do this use the `-d` flag:

```
docker run -d --restart --network=host -e "MURAKAMI_EXPORTERS_LOCAL_TYPE=local" -e "MURAKAMI_EXPORTERS_LOCAL_ENABLED=true" -e "MURAKAMI_EXPORTERS_LOCAL_PATH=/data/" --volume /root/data:/data/ measurementlab/murakami:latest  --immediate
```

This will print the ID of your container and return to your command prompt. It
will look something like this:
`27ad15bfab4b1242537147f266ee06eb9eb7658bb64d576bfb99dd4e47c53c53`. To view the
running logs of that container: `docker logs --follow
27ad15bfab4b1242537147f266ee06eb9eb7658bb64d576bfb99dd4e47c53c53`. When you're
done viewing logs, type `Ctrl-c`.

Optionally, you can add all your environment variables to a local file and use
that in your `docker run` command instead of entering them all on the command
line. For example, copy the file `configs/murakami.config.example` and customize
the values to your needs. As an example, save the file as `env-vars` with these
variables set:

```
MURAKAMI_EXPORTERS_LOCAL_TYPE=local
MURAKAMI_EXPORTERS_LOCAL_ENABLED=true
MURAKAMI_EXPORTERS_LOCAL_PATH=/data/
```
Then run: `docker run --env-file env-vars --network=host --volume /root/data:/data/ measurementlab/murakami:latest --immediate`

You may also define your configuration in a `.toml` formatted file. Make a copy of
`configs/murakami.toml.example` and customize it to your needs, and save this
file in a directory that will be accessible to the container (in this case, we
copied ours into the `configs` folder) and then use this command to start the container:

```
docker run -d --network host --volume /root/data:/var/lib/murakami/ --volume /root/configs:/murakami/configs/ measurementlab/murakami:latest -c /murakami/configs/murakami.toml
```

#### Using the Secure Copy Protocol (SCP) and/or Google Cloud Storage Storage (GCS) Exporters

Each individual test result file can be sent to one or more remote central
storage locations, using available **exporters**. Currently Murakami provides
two remote storage exporters: Secure Copy Protocol (SCP) and Google Cloud
Storage (GCS). Multiple exporters of both types can be used.

Using the SCP and GCS exporters requires additional setup on the remote SCP
server for SCP, and in your Google Cloud Storage project fof GCS:

* **SCP exporter**: requires the username which has access to login to the
  remote server via SSH, and that user's private SSH key. We created a unique
  SSH user and key for our testing.
* **GCS exporter**: requires a [Google Cloud Platform
  Project](https://cloud.google.com/docs/overview/), a [Storage
  Bucket](https://cloud.google.com/storage/docs/), and a [Service
  Account](https://cloud.google.com/iam/docs/creating-managing-service-accounts)
  with the IAM Roles: _Storage Object Creator_, _Storage Object Viewer_, and
  _Storage Legacy Bucket Writer_. We reommend applying these roles for the
  Storage Bucket only, and not project-wide. See Google's [IAM best practice
  guides](https://cloud.google.com/blog/products/gcp/iam-best-practice-guides-available-now)
  for more information. An exported [service account
  key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
  is also required.

Once the SCP private/public key and/or GCS service account key are created, copy
them into the `configs` folder. 

To enable one or more SCP or GCS exporters, customize the appropriate exporter variables in
your copy of `configs/murakami.toml.example` or
`configs/murakami.config.example` and then use one of the commands below to run
the container:

`docker run --env-file /root/env_vars --network=host --volume /root/data:/var/lib/murakami/ --volume /root/configs:/murakami/configs/ measurementlab/murakami:latest`

`docker run --network=host --volume /root/data:/var/lib/murakami/ --volume /root/configs:/murakami/configs/ measurementlab/murakami:latest -c /murakami/configs/murakami.toml`

#### Enabling/Disabling Individual Test Runners

You can define which tests a Murakami container should run using environment
variables or configuration file values.

Again, customize the appropriate variables in your copy of `configs/murakami.toml.example`
or `configs/murakami.config.example` before running the container.

If you are using the `ndt5custom` or `ndt7custom` test runners, you will also
need to create a configuration file containing your list of servers, add that
configuration file to `configs/` and set the path to that file for the custom
runners config variable. You can review and customize the file `configs/ndt-custom-config.json.example` as a starting point.

## Updating Murakami

For standalone Murakami deployments, update your Murakami installations by:
* Log into each device, stop the `murakami` Docker container
* Pull the `latest` Murakami image from Dockerhub
* Ensure your configuration files, key files, and/or service account files are
  present in your local system
* Start the updated `murakami` Docker container
