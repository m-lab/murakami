#!/bin/bash
#
# This script is intended to be run once to setup GCP resources 
# for a new measurement program that uses Murakami.

usage="$0 <project> <bucket> <dataset>"
gcp_project=${1:?Please provide the GCP project: ${usage}}
gcs_bucket=${2:?Please provide the GCS bucket: ${usage}}
bq_dataset=${3:?Please provide the dataset name: ${usage}}

# Set table names
bq_ndt7_table="ndt7"
bq_ndt5_table="ndt5"
bq_speedtest_table="speedtest"

# Create the GCS bucket if it doesn't exist.
buckets=$(gsutil ls)
mybucket=$gcs_bucket

if [[ "$buckets" == *"gs://$mybucket"* ]]; then
	echo "This GCS bucket already exists: $mybucket"
else
  gsutil mb gs://$mybucket
fi

# Create the dataset if it doesn't exist.
bq show $bq_dataset || bq mk $bq_dataset
wait

# Make tables if they don't already exist.
## ndt7 
ndt7exists=$(bq query "SELECT size_bytes FROM $bq_dataset.__TABLES__ WHERE table_id='$bq_ndt7_table'")
if [ -z ${ndt7exists} ]; then
   echo "Creating $bq_ndt7_table in $gcp_project.$bq_dataset."
   bq mk -t --description="Murakami ndt7 results table." \
   $gcp_project:$bq_dataset.$bq_ndt7_table schemas/ndt7Schema.json
fi

## ndt5
ndt5exists=$(bq query "SELECT size_bytes FROM $bq_dataset.__TABLES__ WHERE table_id='$bq_ndt5_table'")
if [ -z ${ndt5exists} ]; then
   echo "Creating $bq_ndt5_table in $gcp_project.$bq_dataset."
   bq mk -t --description="Murakami ndt5 results table." \
   $gcp_project:$bq_dataset.$bq_ndt5_table schemas/ndt5Schema.json
fi

## speedtest
speedtestExists=$(bq query "SELECT size_bytes FROM $bq_dataset.__TABLES__ WHERE table_id='$bq_speedtest_table'")
if [ -z ${speedtestExists} ]; then
   echo "Creating $bq_speedtest_table in $gcp_project.$bq_dataset."
   bq mk -t --description="Murakami speedtest results table." \
   $gcp_project:$bq_dataset.$bq_speedtest_table schemas/speedtestSchema.json
fi

## Supporting table - locations_metadata
locationsMetaExists=$(bq query "SELECT size_bytes FROM $bq_dataset.__TABLES__ WHERE table_id='locations_metadata'")
if [ -z ${locationsMetaExists} ]; then
   echo "Creating locations_metadata in $gcp_project.$bq_dataset."
   bq mk -t --description="Metadata for locations being measured." \
   $gcp_project:$bq_dataset.locations_metadata schemas/locationsMetaSchema.json
fi


# Make views

## device_metadata
bq mk --use_legacy_sql=false \
--description "a view summarizing metadata about devices measuring in a murakami fleet" \
--view \
"WITH
ndt5 AS 
(SELECT MurakamiDeviceID, MurakamiLocation, MurakamiConnectionType,
MurakamiNetworkType FROM \`${gcp_project}.${bq_dataset}.${bq_ndt5_table}\`
GROUP BY MurakamiDeviceID, MurakamiLocation, MurakamiConnectionType,
MurakamiNetworkType ),
ndt7 AS 
(SELECT MurakamiDeviceID, MurakamiLocation, MurakamiConnectionType, 
MurakamiNetworkType FROM \`${gcp_project}.${bq_dataset}.${bq_ndt5_table}\`
GROUP BY MurakamiDeviceID, MurakamiLocation, MurakamiConnectionType,
MurakamiNetworkType ),
speedtest AS 
(SELECT MurakamiDeviceID, MurakamiLocation, MurakamiConnectionType, MurakamiNetworkType FROM \`${gcp_project}.${bq_dataset}.${bq_ndt5_table}\`
GROUP BY MurakamiDeviceID, MurakamiLocation, MurakamiConnectionType,
MurakamiNetworkType )
SELECT * FROM ${bq_ndt5_table} GROUP BY MurakamiDeviceID, MurakamiLocation,
MurakamiConnectionType, MurakamiNetworkType
UNION DISTINCT (SELECT * FROM ${bq_ndt7_table})
UNION DISTINCT (SELECT * FROM ${bq_speedtest_table})" \
$bq_dataset.device_metadata

## server_coordinates

bq mk --use_legacy_sql=false \
--description "a view identifying the locations of all servers used to conduct tests and some metadata about each server." \
--view \
"WITH
mlabsites AS (
  SELECT transit.asn AS asn, location.city AS city, location.country_code AS country, 
  network.ipv4.prefix AS ipv4_prefix, network.ipv6.prefix AS ipv6_prefix, location.metro AS metro, 
  name, transit.provider AS provider, transit.uplink AS uplink, CONCAT(location.latitude,',',location.longitude) AS coordinates 
  FROM \`mlab-collaboration.platform_meta.mlab_site_info\`
),
locations_meta AS (
  SELECT MurakamiDeviceID, MurakamiDeviceMetadata1, MurakamiDeviceMetadata2, LocName, LocSecondaryName, LocTertiaryName, CountryName, CountryCode, TimeZone, LatLon, Isp1Name, Isp1Type, Isp1AccessMedia, Isp1ASN, Isp1ASName, Isp1ServicePlan, Isp1ServiceCost, Isp1ServiceCostUnits, Isp2Name, Isp2Type, Isp2AccessMedia, Isp2ASN, Isp2ASName, Isp2ServicePlan, Isp2ServiceCost, Isp2ServiceCostUnits
  FROM \`${gcp_project}.${bq_dataset}.locations_metadata\`
),
ndt5_client_server AS (
  SELECT TestName, tests.MurakamiLocation, locations_meta.LatLon AS location_lat_lon, ClientIP, ServerIP, 
  ServerName, 
  mlabsites.coordinates AS server_lat_lon,
  mlabsites.provider AS host,
  CONCAT(mlabsites.city, ', ', mlabsites.country) AS ServerLocation
  FROM \`${gcp_project}.${bq_dataset}.${bq_ndt5_table}\` tests, 
   mlabsites, locations_meta
  WHERE ServerName LIKE CONCAT('%',mlabsites.name,'%')
  AND tests.MurakamiDeviceID = locations_meta.MurakamiDeviceID
  GROUP BY TestName, MurakamiLocation, location_lat_lon, ClientIP, ServerIP, 
  ServerName, server_lat_lon, host, ServerLocation
),
ndt7_client_server AS (
  SELECT TestName, tests.MurakamiLocation, locations_meta.LatLon AS location_lat_lon, ClientIP, ServerIP, 
  ServerName, 
  mlabsites.coordinates AS server_lat_lon, 
  mlabsites.provider AS host,
  CONCAT(mlabsites.city, ', ', mlabsites.country) AS ServerLocation
  FROM \`${gcp_project}.${bq_dataset}.${bq_ndt7_table}\` tests, 
   mlabsites, locations_meta
  WHERE ServerName LIKE CONCAT('%',mlabsites.name,'%')
  AND tests.MurakamiDeviceID = locations_meta.MurakamiDeviceID
  GROUP BY TestName, MurakamiLocation, location_lat_lon, ClientIP, ServerIP, 
  ServerName, server_lat_lon, host, ServerLocation
),
speedtest_client_server AS (
  SELECT TestName, tests.MurakamiLocation, locations_meta.LatLon AS location_lat_lon, ClientIP, '' AS ServerIP, 
  ServerURL AS ServerName, 
  CONCAT(ServerLat, ', ', ServerLon) AS server_lat_lon, ServerSponsor AS host, ServerName AS ServerLocation
  FROM \`${gcp_project}.${bq_dataset}.${bq_speedtest_table}\` tests, locations_meta
  GROUP BY TestName, MurakamiLocation, location_lat_lon, ClientIP, ServerIP, 
  ServerURL, server_lat_lon, host, ServerLocation
)
SELECT * FROM ndt5_client_server
GROUP BY TestName, MurakamiLocation, location_lat_lon, ClientIP, ServerIP, 
ServerName, server_lat_lon, host, ServerLocation
UNION ALL (SELECT * FROM ndt7_client_server)
UNION ALL (SELECT * FROM speedtest_client_server)" $bq_dataset.server_coords

## Unified view of performance tests

bq mk --use_legacy_sql=false \
--description "a view combining supported performance tests: ndt5, ndt7, speedtest single, & speedtest multi, with client & server location metadata" \
--view \
"
WITH
device_metadata AS (
  SELECT * FROM \`${gcp_project}.${bq_dataset}.device_metadata\`
),
locations_meta AS (
  SELECT MurakamiDeviceID, MurakamiDeviceMetadata1, MurakamiDeviceMetadata2, LocName, LocSecondaryName, LocTertiaryName, CountryName, CountryCode, TimeZone, LatLon, Isp1Name, Isp1Type, Isp1AccessMedia, Isp1ASN, Isp1ASName, Isp1ServicePlan, Isp1ServiceCost, Isp1ServiceCostUnits, Isp2Name, Isp2Type, Isp2AccessMedia, Isp2ASN, Isp2ASName, Isp2ServicePlan, Isp2ServiceCost, Isp2ServiceCostUnits
  FROM \`${gcp_project}.${bq_dataset}.locations_metadata\`
),
mlabsites AS (
  SELECT transit.asn AS asn, location.city AS city, location.country_code AS country, 
  network.ipv4.prefix AS ipv4_prefix, network.ipv6.prefix AS ipv6_prefix, location.metro AS metro, 
  name, transit.provider AS provider, transit.uplink AS uplink, CONCAT(location.latitude,',',location.longitude) AS coordinates 
  FROM \`mlab-collaboration.platform_meta.mlab_site_info\`
),
server_coords AS (
  SELECT * FROM \`${gcp_project}.${bq_dataset}.server_coords\`
),
ndt5 AS (
  SELECT TestName, DATETIME(TestStartTime, TimeZone) AS TestStartTime, tests.MurakamiLocation, 
  MurakamiConnectionType, MurakamiNetworkType, tests.MurakamiDeviceID, DownloadValue, DownloadUnit, 
  UploadValue, UploadUnit, MinRTTValue, MinRTTUnit, meta.MurakamiDeviceMetadata1, meta.MurakamiDeviceMetadata2, meta.LocName, meta.LocSecondaryName, meta.LocTertiaryName, meta.CountryName, meta.CountryCode, meta.TimeZone, meta.LatLon, meta.Isp1Name, meta.Isp1Type, meta.Isp1AccessMedia, meta.Isp1ASN, meta.Isp1ASName, meta.Isp1ServicePlan, meta.Isp1ServiceCost, meta.Isp1ServiceCostUnits, meta.Isp2Name, meta.Isp2Type, meta.Isp2AccessMedia, meta.Isp2ASN, meta.Isp2ASName, meta.Isp2ServicePlan, meta.Isp2ServiceCost, meta.Isp2ServiceCostUnits, CAST(ClientIP AS STRING) AS ClientIP, 
  DownloadUUID, CAST(ServerIP AS STRING) AS ServerIP, ServerName, mlabsites.coordinates AS server_lat_lon, 
  mlabsites.provider AS host, CONCAT(mlabsites.city, ', ', mlabsites.country) AS ServerLocation
  FROM \`${gcp_project}.${bq_dataset}.${bq_ndt5_table}\` tests, locations_meta meta, mlabsites
  WHERE tests.MurakamiDeviceID = meta.MurakamiDeviceID
  AND ServerName LIKE CONCAT('%',mlabsites.name,'%')
),
ndt7 AS (
  SELECT TestName, DATETIME(TestStartTime, TimeZone) AS TestStartTime, tests.MurakamiLocation, 
  MurakamiConnectionType, MurakamiNetworkType, tests.MurakamiDeviceID, DownloadValue, DownloadUnit, 
  UploadValue, UploadUnit, MinRTTValue, MinRTTUnit, meta.MurakamiDeviceMetadata1, meta.MurakamiDeviceMetadata2, meta.LocName, meta.LocSecondaryName, meta.LocTertiaryName, meta.CountryName, meta.CountryCode, meta.TimeZone, meta.LatLon, meta.Isp1Name, meta.Isp1Type, meta.Isp1AccessMedia, meta.Isp1ASN, meta.Isp1ASName, meta.Isp1ServicePlan, meta.Isp1ServiceCost, meta.Isp1ServiceCostUnits, meta.Isp2Name, meta.Isp2Type, meta.Isp2AccessMedia, meta.Isp2ASN, meta.Isp2ASName, meta.Isp2ServicePlan, meta.Isp2ServiceCost, meta.Isp2ServiceCostUnits, CAST(ClientIP AS STRING) AS ClientIP, 
  DownloadUUID, CAST(ServerIP AS STRING) AS ServerIP, ServerName, mlabsites.coordinates AS server_lat_lon, 
  mlabsites.provider AS host, CONCAT(mlabsites.city, ', ', mlabsites.country) AS ServerLocation
  FROM \`${gcp_project}.${bq_dataset}.${bq_ndt7_table}\` tests, locations_meta meta, mlabsites
  WHERE tests.MurakamiDeviceID = meta.MurakamiDeviceID
  AND ServerName LIKE CONCAT('%',mlabsites.name,'%')
),
speedtest AS (
  SELECT TestName, DATETIME(TestStartTime, TimeZone) AS TestStartTime, tests.MurakamiLocation, 
  MurakamiConnectionType, MurakamiNetworkType, tests.MurakamiDeviceID, DownloadValue/1000000 AS DownloadValue, 
  DownloadUnit, UploadValue/1000000 AS UploadValue, UploadUnit, Ping AS MinRTTValue, PingUnit AS MinRTTUnit, meta.MurakamiDeviceMetadata1, meta.MurakamiDeviceMetadata2, meta.LocName, meta.LocSecondaryName, meta.LocTertiaryName, meta.CountryName, meta.CountryCode, meta.TimeZone, meta.LatLon, meta.Isp1Name, meta.Isp1Type, meta.Isp1AccessMedia, meta.Isp1ASN, meta.Isp1ASName, meta.Isp1ServicePlan, meta.Isp1ServiceCost, meta.Isp1ServiceCostUnits, meta.Isp2Name, meta.Isp2Type, meta.Isp2AccessMedia, meta.Isp2ASN, meta.Isp2ASName, meta.Isp2ServicePlan, meta.Isp2ServiceCost, meta.Isp2ServiceCostUnits,
  CAST(ClientIP AS STRING) AS ClientIP, '' AS DownloadUUID, '' AS ServerIP, ServerURL AS ServerName, 
  CONCAT(ServerLat, ', ', ServerLon) AS server_lat_lon, ServerSponsor AS host, ServerName AS ServerLocation
  FROM \`${gcp_project}.${bq_dataset}.${bq_speedtest_table}\` tests, locations_meta meta
  WHERE tests.MurakamiDeviceID = meta.MurakamiDeviceID
),
combined_results AS (
  SELECT * FROM ndt5
  UNION ALL (SELECT * FROM ndt7 )
  UNION ALL (SELECT * FROM speedtest)
)
SELECT * FROM combined_results" $bq_dataset.unified_perf_tests

wait

## Max speeds per test, location, & user supplied metadata.

bq mk --use_legacy_sql=false \
--description "a view providing the maximum measured speeds test, location, and user supplied metadata values." \
--view \
"SELECT
MurakamiLocation, TestName, MurakamiConnectionType, MurakamiNetworkType, 
ROUND(MAX(DownloadValue),2) AS MaxDownload, ROUND(MAX(UploadValue),2) AS MaxUpload
FROM \`${gcp_project}.${bq_dataset}.unified_perf_tests\`
GROUP BY MurakamiLocation, TestName, MurakamiConnectionType, MurakamiNetworkType
ORDER BY MurakamiLocation, TestName, MurakamiConnectionType, MurakamiNetworkType" $bq_dataset.max_by_test_location_metadata

wait

## Max speeds per test, aggregated by month

bq mk --use_legacy_sql=false \
--description "a view providing the maximum measured speeds by month and test" \
--view \
"SELECT
FORMAT_DATE('%Y-%m',TestStartTime) AS YearMonth, MurakamiLocation, MurakamiConnectionType, MurakamiNetworkType, TestName,
ROUND(MAX(DownloadValue),2) AS MaxDownload, ROUND(MAX(UploadValue),2) AS MaxUpload
FROM \`${gcp_project}.${bq_dataset}.unified_perf_tests\`
GROUP BY YearMonth, MurakamiLocation, MurakamiConnectionType, MurakamiNetworkType, TestName
ORDER BY YearMonth, MurakamiLocation, MurakamiConnectionType, MurakamiNetworkType, TestName" $bq_dataset.max_by_month_test
