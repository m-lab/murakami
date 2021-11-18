# Murakami on Google Cloud Demo

Utility scripts that provide some automation to setup Google Cloud resources and
provisioning new devices for a Balena Cloud fleet are available in `utilities/`.
These are designed to support M-Lab demo fleets, so please inspect and customize
them to your liking.

* `setup_bq.sh` - Intended to be run once to setup GCP resources for a new
  measurement program or demo. The Google Cloud SDK must be installed and
  authorized with an account that has IAM permissions to create GCS buckets
  and BigQuery datasets, tables and views.
* `setup_balena_device.sh` - This script can be used to provision new Murakami devices in
  your Balena Cloud fleet. It requires the balena-cli to be installed and
  authorized.
* `bq_load_murakami.sh` - Intended to be scheduled daily using scheduled jobs or
  cron, this script will load murakami test results files within a GCS bucket
  from the previous day into BigQuery tables.