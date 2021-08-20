#!/bin/bash
#
# This script is intended to be run once to setup GCP resources 
# for a new measurement program that uses Murakami.

# Set the variables below for your installation
gcp_project="<gcp project>"
bq_dataset="<bigquery dataset>"
bq_ndt7_table="ndt7"
bq_ndt5_table="ndt5"
bq_speedtest_table="speedtest"

# Create the dataset if it doesn't exist.
bq show $bq_dataset || bq mk $bq_dataset
wait

# Make tables if they don't already exist.
## ndt7 
ndt7exists=`bq query "SELECT size_bytes FROM $bq_dataset.__TABLES__ WHERE table_id='$bq_ndt7_table'"`
if [ -z ${ndt7exists} ]; then
   echo "Creating $bq_ndt7_table in $gcp_project.$bq_dataset."
   bq mk -t --description="Murakami ndt7 results table." \
   $gcp_project:$bq_dataset.$bq_ndt7_table schemas/ndt7Schema.json
fi

## ndt5
ndt5exists=`bq query "SELECT size_bytes FROM $bq_dataset.__TABLES__ WHERE table_id='$bq_ndt5_table'"`
if [ -z ${ndt5exists} ]; then
   echo "Creating $bq_ndt5_table in $gcp_project.$bq_dataset."
   bq mk -t --description="Murakami ndt5 results table." \
   $gcp_project:$bq_dataset.$bq_ndt5_table schemas/ndt5Schema.json
fi

## speedtest
speedtestExists=`bq query "SELECT size_bytes FROM $bq_dataset.__TABLES__ WHERE table_id='$bq_speedtest_table'"`
if [ -z ${speedtestExists} ]; then
   echo "Creating $bq_speedtest_table in $gcp_project.$bq_dataset."
   bq mk -t --description="Murakami speedtest results table." \
   $gcp_project:$bq_dataset.$bq_speedtest_table schemas/speedtestSchema.json
fi
