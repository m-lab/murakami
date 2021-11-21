# Murakami Google Cloud Demo

Included in `utilities/` are several bash scripts that have supported the setup
of Murakami device fleets for testing and demonstration purposes. The scripts
provide some automation to setup a Murakami demo consisting of:

* Murakami measurement devices within a Balena Cloud managed fleet
* Exported test results to a Google Cloud Storage bucket
* Cron or scheduled task to post test results to tables in a BigQuery dataset
* BigQuery Views to provide more detailed metadata and combined results which
  support visualization within DataStudio

Currently these utilities support the ndt5, ndt7, and speedtest-cli test
runners and are provided as examples, not as a supported part of Murakami.
Please inspect them, customize, and use if helpful to support your needs.

* `setup_balena_device.sh` - This script can be used to provision new Murakami devices in
  your Balena Cloud fleet. It requires the balena-cli to be installed and
  authorized. Run each time a new device needs to be added to a fleet.

* `setup_bq.sh` - Intended to be run once to setup GCP resources for a new
  measurement program or demo. The Google Cloud SDK must be installed and
  authorized with an account that has IAM permissions to create GCS buckets
  and BigQuery datasets, tables and views in your Google Cloud Project.

* `bq_load_murakami.sh` - Intended to be scheduled daily using scheduled jobs or
  cron, this script will load murakami test results files within a GCS bucket
  from the previous day into BigQuery tables.
