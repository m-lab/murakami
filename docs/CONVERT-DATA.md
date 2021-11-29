# Converting Murakami Data to CSV

When using the local, GCS, or SCP exporters that come with Murakami, each test
result is saved as a single JSON file. JSON is a great format for machines to
process data, but users may wish to analyze all collected data in other
programs, so we've included a utility script in Murakami that converts the
results for each supported test runner to CSV format.

## Using the murakami-convert Utility Script

In the main folder of the Murakami repo, you'll see `scripts/convert.py`. This
Python utility script will convert test results from supported runners from JSON
to CSV. Below we'll run through one example of how to use it.

Download or navigate on the command line to the location where you've saved your
test results. In our case, we are using the GCS exporter to push all test
results to a common archive location. To convert these files to CSV, we first
downloaded all the test results for a particular location from GCS to our local
computer.

Next, we can run the Murakami Docker container on our local computer, and mount
the folder containing our test results inside it.

`docker run -it --entrypoint /bin/bash --volume /path/to/test-results:/data/ measurementlab/murakami:latest`

That command will pull the latest Murakami image from M-Lab's Dockerhub, and
drop you into a terminal: `root@714d9de32802:/murakami#`

You should then be able to see your test results: `root@714d9de32802:/murakami# ls -la /data/`

Create a folder to save your converted CSV files: ``root@714d9de32802:/murakami# mkdir /data/csv`

Now you can use `murakami-convert` to convert the results of each test runner.
To review all the available script options, type: `murakami-convert --help`

Below are examples converting the different supported test runners. Note that
your filenames are likely different than our example, so you should adjust the
last part of these commands to match the naming patterns of your files.

* ndt5 - `root@714d9de32802:/murakami# murakami-convert -t ndt5 -r -o /data/csv/ndt5-egress.csv /data/ndt5*`
* ndt7 - `root@714d9de32802:/murakami# murakami-convert -t ndt7 -r -o /data/csv/ndt7-egress.csv /data/ndt5*`
* speedtest-cli single stream - `root@714d9de32802:/murakami# murakami-convert -t speedtest -r -o /data/csv/speedtest-cli-singlestream-egress.csv /data/speedtest-single*`
* speedtest-cli multi stream - `root@714d9de32802:/murakami# murakami-convert -t speedtest -r -o /data/csv/speedtest-cli-multistream-egress.csv /data/speedtest-multi*`

When you're done converting your files, exit the container. The CSVs should now
be in the csv folder where you exported them.

