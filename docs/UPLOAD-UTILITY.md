# Uploading Previously Collected Test Data to an Instance of Murakami-Viz

[Murakami-Viz](https://github.com/m-lab/murakami-viz/) is a separate data visualization service that can optionally be used with Murakami measurement devices, particularly a fleet of devices managed through Balena.io.

Included with Murakami is a utility script, **murakami-upload** found in `scripts/murakami-upload.py`, that provides a means of uploading previously collected test results from Murakami's NDT or Speedtest-CLI runners to an instance of Murakami-Viz.

For `murakami-upload` to successfully upload results to a Murakami Viz instance:
* all test result files must contain the MurakamiDeviceID field
* each device ID must be associated with a measurement device in the Murakami-Viz instance
* the current, public IP address of the computer you’ll use to run murakami-upload must be whitelisted in the Murakami-Viz instance

## How to Use murakami-upload

* Obtain test data from missing dates
* Enter or Start an interactive Murakami container containing the missing test data
* Run murakami-upload
* Confirm data was received by the Murakami-Viz instance

### Obtain test data from on-device or exported locations

Depending on the export locations configured for your Murakami measurement device, test results may be stored in one or more locations.

#### On-Device Data

To upload test data that is stored on a Murakami measurement device, first login to the device itself. If this is a Balena Cloud managed device, you can use the terminal through your Balena app or the balena-cli tool to login to the main container. If this is a standalone device, SSH to the device.

In either case, when you’re on the device’s terminal, first confirm that murakami-upload is a usable program in the Murakami release running on the device.

```
root@d9fa4d8:/murakami# ls scripts/
convert.py  upload.py
root@d9fa4d8:/murakami# which murakami-upload
/usr/local/bin/murakami-upload
```

To learn more about how to use murakami-upload, type: `murakami-upload -h`

```
murakami-upload -h
usage: murakami-upload [-h] [-p PATH] [-u URL]
Uploads JSON results via HTTPExporter
optional arguments:
  -h, --help           show this help message and exit
  -p PATH, -path PATH  input path
  -u URL, -url URL     URL to send JSON data to
```

On a Balena managed device with the local exporter enabled, test result data will be in `/data/`

To upload results from Nov. 9-17, 2020, we might upload all test results from all test runners, one day at a time using a command such as:

`murakami-upload -p '/data/*2020-11-09*' -u '<ip address or hostname>/api/v1/runs'`

When you run the murakami-upload script, the environment variables available on the device are printed in the terminal output, followed by successful status messages such as those listed below:

```
Reading path /data/*2020-11-09*
Files: ['/data/speedtest-cli-multi-stream-mlab-testbed-home-wired-2020-11-09T17:49:02.633159.jsonl', '/data/ndt5-mlab-testbed-home-wired-2020-11-09T17:48:09.359179.jsonl', '/data/ndt7-mlab-testbed-home-wired-2020-11-09T17:48:36.805318.jsonl', '/data/speedtest-cli-single-stream-mlab-testbed-home-wired-2020-11-09T17:49:45.946055.jsonl', '/data/ndt7-mlab-testbed-home-wired-2020-11-09T17:46:34.017050.jsonl']
```

Within a few minutes of completion, the uploaded data should be available in your instance of Murakami-Viz.

### Data from GCS or SCP Server Archive

If you’ve exported your data to GCS or an SCP server, you can use murakami-upload from a Docker container on any computer to send it to a running instance of Murakami-Viz.

First, obtain a local copy of the test data you wish to upload to your instance of Murakami-Viz. For demonstration purposes, we have created a folder called `murakami-upload` and a subfolder, `data`, on our local computer. We then copied some test result files from GCS into the `data` folder.

Next, we will run a Murakami container locally (not on a test device, but on your computer), and mount the `data` folder as a volume within it. The command below is an example which you can customize for the paths to your data folder:

`docker run -it --entrypoint /bin/bash --volume /path/to/test-results:/data/ measurementlab/murakami:latest`

The command pulls the latest Murakami image from M-Lab’s Dockerhub if needed, and once completed will provide a terminal inside the container. You can then confirm the data you plan to upload is available in the container, and finally upload it to your Murakami-Viz server with the same command as in the previous section. Below is an abbreviated log of terminal output showing these steps.

```
Unable to find image 'measurementlab/murakami:latest' locally
latest: Pulling from measurementlab/murakami
6c33745f49b4: Pull complete
ef072fc32a84: Pull complete
...
e72eb1440e38: Pull complete
Digest: sha256:30a762371c521b658b75d274c6561481d5244e3bda5e90778279129015673b0e
Status: Downloaded newer image for measurementlab/murakami:latest
root@0caf99b798d6:/murakami#
root@0caf99b798d6:/murakami# ls /data
ndt5-mlab-testbed-home-wired-2020-11-09T09:27:26.197005.jsonl
ndt5-mlab-testbed-home-wired-2020-11-09T11:06:35.118214.jsonl
ndt5-mlab-testbed-home-wired-2020-11-09T12:48:38.150086.jsonl
...
murakami-upload -p '/data/*2020-11-09*' -u 'https://viz.measuringbroadband.org/api/v1/runs'
```

Within a few minutes of completion, the uploaded data should be available in your instance of Murakami-Viz.
