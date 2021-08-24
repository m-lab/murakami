#!/bin/bash
#
# This script is intended to be run daily using a scheduled job/cron,
# and loads test results from the GCS bucket where Murakami devices are
# exporting to tables in BigQuery.
#
# A service account or personal Google account running this script
# requires these permissions in your project:  
#  BigQuery Job User, BigQuery Data Editor, Storage Object Viewer

usage="$0 <project> <bucket> <dataset>"
gcp_project=${1:?Please provide the GCP project: ${usage}}
gcs_bucket=${2:?Please provide the GCS bucket: ${usage}}
bq_dataset=${3:?Please provide the dataset name: ${usage}}

bq_ndt7_table="ndt7"
bq_ndt5_table="ndt5"
bq_speedtest_table="speedtest"

# Load data from yesterday in UTC
loaddate=`date -d "$date - 1 day" +"%Y-%m-%d"`

# NDT 7 loader

for f in `gsutil ls gs://$gcs_bucket/ndt7*$loaddate*`
do
   bq load --source_format=NEWLINE_DELIMITED_JSON \
   --project_id=$gcp_project $bq_dataset.$bq_ndt7_table $f \
   schemas/ndt7Schema.json
done

# NDT 5 loader
for f in `gsutil ls gs://$gcs_bucket/ndt5*$loaddate*`
do
   bq load --source_format=NEWLINE_DELIMITED_JSON \
   --project_id=$gcp_project $bq_dataset.$bq_ndt5_table $f \
   schemas/ndt5Schema.json
done

# Speedtest-cli loader
for f in `gsutil ls gs://$gcs_bucket/speedtest-cli*$loaddate*`
do
   bq load --source_format=NEWLINE_DELIMITED_JSON \
   --project_id=$gcp_project $bq_dataset.$bq_speedtest_table $f \
   schemas/speedtestSchema.json
done
