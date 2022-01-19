# Installation and Use - Murakami Containers on One or More Balena Cloud Manged Devices

M-Lab supports management of a fleet of Murakami devices using [Balena
Cloud](https://balena.io). Murakami containers for use with Balena Cloud are
built using the `Dockerfile.template` file in the main directory of this repository.

## Supported System Architectures for Balena Cloud Managed Murakami Devices

Murakami has been tested using devices of the following architectures on Balena
Cloud.

* armv7hf
* aarch64

## Quick Setup for Balena Cloud Managed Murakami Deployment

1. Clone the Murakami repo from Gitub
2. Setup your project on Balena.io
3. [Install](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md) the `balena-cli` tool
4. Install BalenaOS for each project device
5. Configure fleet-wide and device-specific variables
6. Push/build release and apply to managed devices

Below we'll cover #5 & #6 for the example we've tested.

## Configuring Fleet-Wide and Device-Specific Variables

To use Murakami on a Balena Cloud managed device, first clone the code
repository to your local machine. The file `Dockerfile.template` will be used to
build the container image on Balena's cloud build servers, and deploy it to your
project devices. This guide will assume you have setup a project on Balena
Cloud.

We recommend configuring Murakami on Balena managed devices using variables
defined in your Balena Cloud project, rather than in a local text or `.toml`
configuration file containing your variables.

In our testing, we have some settings that apply to all devices in the
Balena Cloud fleet, and others that apply to each individual device.

We set the following fleet-wide variables:

```
NAME                             VALUE
MURAKAMI_EXPORTERS_GCS_TYPE      gcs
MURAKAMI_EXPORTERS_LOCAL_ENABLED 1
MURAKAMI_EXPORTERS_LOCAL_PATH    /data/
MURAKAMI_EXPORTERS_LOCAL_TYPE    local
MURAKAMI_EXPORTERS_GCS_ACCOUNT   your-gcp-service-account@your-gcp-project.iam.gserviceaccount.com
MURAKAMI_EXPORTERS_GCS_ENABLED   1
MURAKAMI_EXPORTERS_GCS_KEY       /murakami/configs/your-service-account-keyfile.json
MURAKAMI_EXPORTERS_GCS_TARGET    gs://your-gcs-bucket/
MURAKAMI_EXPORTERS_SCP_TYPE      scp
MURAKAMI_EXPORTERS_SCP_ENABLED   1
MURAKAMI_EXPORTERS_SCP_KEY       /murakami/configs/ssh-private-key-filename
MURAKAMI_EXPORTERS_SCP_PORT      22
MURAKAMI_EXPORTERS_SCP_TARGET    our-scp-server-hostname-or-IP-address:murakami-exported-data/
MURAKAMI_EXPORTERS_SCP_USERNAME  your-scp-username
```

And these values, specific to an individual Murakami device:

```
MURAKAMI_SETTINGS_WEBTHINGS       0
MURAKAMI_SETTINGS_PORT            80
MURAKAMI_SETTINGS_LOGLEVEL        INFO
MURAKAMI_SETTINGS_IMMEDIATE       1
MURAKAMI_SETTINGS_LOCATION        mydevicelocation
MURAKAMI_SETTINGS_NETWORK_TYPE    home
MURAKAMI_SETTINGS_CONNECTION_TYPE wired
```

In this example, we can define the same exporters for all Balena managed devices
using fleet level variables, so that all data goes to one or more centralized
locations. And using the second set of variables applied to the individual
device lets us customize the variables used in naming output files:
LOCATION, CONNECTION_TYPE, and NETWORK_TYPE.

## Push/Build Balena Cloud Project Release

Pushing a release to your Balena Cloud fleet is straightforward. If you're
using SCP and/or GCS exporters, as with the [Standalone Murakami](https://github.com/m-lab/murakami/blob/master/docs/INSTALL-MURAKAMI-STANDALONE.md) device, when
using SCP and GCS exporters, the relevant key files need to be accessible in the
container. 

Add your GCS service account keyfile and/or your SCP private key to the folder: `configs/`

Then kick off a container build for your Balena Cloud project:
`balena push your-balena-fleet-name -c`

The `-c` flag tells Balena to not use previously cached container layers.

## Updating Murakami

For Balena Cloud fleet deployments, update your Murakami installations by:
* Pulling recent changes from `m-lab/murakami` master branch into your local
  copy, fork, or merge upstream changes into your fork/branch.
* Ensure your configuration files, key files, and/or service account files are
  present in your local system
* Push a new release to your Balena Cloud fleet
