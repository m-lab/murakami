# Installation and Use - Murakami Containers on One or More Balena Cloud Manged Devices

M-Lab supports management of a fleet of Murakami devices using the [Balena Cloud](https://balena.io).

## Supported System Architectures for Balena Cloud managed Murakami Devices

* armv7hf

## Quick Setup for Balena Cloud Managed Murakami Deployment

1. Clone the murakami repo from Gitub
2. Setup your project on Balena.io
3. [Install](https://github.com/balena-io/balena-cli/blob/master/INSTALL.md) the `balena-cli` tool
4. Install BalenaOS for each project device
5. Configure project wide and device specific environment variables
6. Push/build release and apply to managed devices

Below we'll cover #5 & #6 for the example we've tested.

## Configuring Project-Wide and Device-Specific Environment Variables

To use Murakami on a Balena Cloud device, first clone the code repository to your local machine. The file `Dockerfile.template` will be used to build the container image on Balena's cloud build servers, and deploy it to your project devices. This guide will assume you have setup a project on Balena Cloud.

We recommend configuring Murakami on Balena Managed devices using environment variables defined in your Balena Cloud project, rather than in a local `.toml` configuration file or in a local file containing your environment variables.

In our testing, we have some settings that should apply to all devices in the Balena Cloud project, and others that should apply to each individual device. 

We set the following values for project-wide Environment Variables:

```
NAME                             VALUE
MURAKAMI_EXPORTERS_GCS_TYPE      gcs
MURAKAMI_EXPORTERS_LOCAL_ENABLED 1
MURAKAMI_EXPORTERS_LOCAL_PATH    /data/
MURAKAMI_EXPORTERS_LOCAL_TYPE    local
MURAKAMI_EXPORTERS_GCS_ACCOUNT   murakami-test-gcs@mlab-sandbox.iam.gserviceaccount.com
MURAKAMI_EXPORTERS_GCS_ENABLED   1
MURAKAMI_EXPORTERS_GCS_KEY       /murakami/keys/murakami-gcs-serviceaccount.json
MURAKAMI_EXPORTERS_GCS_TARGET    gs://murakami-gcs-test/
MURAKAMI_EXPORTERS_SCP_ENABLED   1
MURAKAMI_EXPORTERS_SCP_KEY       /murakami/keys/id_rsa_murakami
MURAKAMI_EXPORTERS_SCP_PORT      22
MURAKAMI_EXPORTERS_SCP_TARGET    remote.host.org:murakami-export-test/
MURAKAMI_EXPORTERS_SCP_TYPE      scp
MURAKAMI_EXPORTERS_SCP_USERNAME  username
```

And these values, specific to an individual Murakami device:

```
MURAKAMI_SETTINGS_PORT            80
MURAKAMI_SETTINGS_LOGLEVEL        DEBUG
MURAKAMI_SETTINGS_HOSTNAME        balena_wifi
MURAKAMI_SETTINGS_IMMEDIATE       1
MURAKAMI_SETTINGS_WEBTHINGS       0
MURAKAMI_SETTINGS_CONNECTION_TYPE wifi_balena
MURAKAMI_SETTINGS_LOCATION        mydevicelocation
MURAKAMI_SETTINGS_NETWORK_TYPE    home
```

In this example, we can define the same exporters for all Balena managed devices using project level environment variables, so that all data goes to one or more centralized locations. And using the second set of variables applied to the individual device lets us customize the variables used in naming output files: LOCATION, CONNECTION_TYPE, and NETWORK_TYPE.

## Push/Build Balena Cloud Project Release

Pushing a release to your Balena Cloud project is straightforward. If you're using SCP and/or GCS exporters, as with the [Standalone Murakami] device, when using SCP and GCS exporters, the relevant key files need to be accessible in the container. 

Following from the example environment variables above, create a `keys` directory in the folder where you've cloned the Murakami repo. Your directory contents should look something like this:

```
$ ls
BUILD.md                           murakami
Dockerfile                         murakami.toml
Dockerfile.template                murakami.toml.example
docs                               poetry.lock
INSTALL-MURAKAMI-BALENA-CLOUD.md   pyproject.toml
INSTALL-MURAKAMI-LOCAL-MANAGED.md  README.md
INSTALL-MURAKAMI-STANDALONE.md     RUN-MURAKAMI-TESTS.md
keys                               RUN-MURAKAMI-WITHOUT-DOCKER.md
LICENSE                            tests

$ ls keys/
murakami-gcs-serviceaccount.json  id_rsa_murakami

```

Then kick off a container build for your Balena Cloud project:
`balena push your-balena-project-name -c`

The `-c` flag tells Balena to not use previously cached container layers.
