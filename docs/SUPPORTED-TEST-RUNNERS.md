# Murakami Supported Test Runners

## NDT

The [Network Diagnostic Tool (NDT)](https://www.measurementlab.net/tests/ndt/)
from M-Lab is a single stream measurement of a connection’s capacity for “bulk
transport” (as defined in IETF’s [RFC
3148](https://tools.ietf.org/html/rfc3148). NDT measures “single stream
performance” or “bulk transport capacity”. NDT reports upload and download
speeds and latency metrics.

M-Lab provides two NDT protocols,
[ndt5](https://www.measurementlab.net/tests/ndt/ndt5) and
[ndt7](https://www.measurementlab.net/tests/ndt/ndt7).

### NDT 5 

Murakami includes M-Lab's [NDT 5 Go
client](https://github.com/m-lab/ndt5-client-go). NDT 5 is the legacy protocol,
measuring a connection's performance using the TCP CUBIC and TCP RENO
compression algorithms. NDT 5 requires a specific set of [network
ports](https://www.measurementlab.net/faq/#what-firewall-ports-does-ndt-require-to-be-open)
to be open in order to run. M-Lab will eventually deprecate the NDT5 protocol
once the NDT7 protocol is adopted and in wider use.

### NDT 7

Murakami includes M-Lab's [NDT 7 Go
client](https://github.com/m-lab/ndt7-client-go). The [NDT 7
protocol](https://github.com/m-lab/ndt-server/blob/master/spec/ndt7-protocol.md)
measures a connection's performance using TCP BBR in networks supporting it. NDT
7 operates solely on either port 80 or 443 and provides a better end-to-end
measurement than past NDT versions.

### NDT 5 / 7 Custom Test Runners

The `ndt5custom` and `ndt7custom` test runners are provided as an alternative to
the standard runners to enable additional features of interest to many
researchers. By default, NDT clients like the standard `ndt5` and `ndt7`
runners, contact the [M-Lab Locate Service](https://www.measurementlab.net/develop/locate-v2/)
to identify several geographically closest and available M-Lab servers to which
the test can be conducted. Geographically closest or nearest in this case is
based on a 

The `ndt5custom` and `ndt7custom` runners provide additional capabilities:

* run tests to self-hosted ndt-servers
* use the M-Lab Locate Service to [select servers](https://github.com/m-lab/locate/blob/master/USAGE.md#how-gcp-identifies-client-location) by I[SO 3166-1 alpha 2 country
  code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) or [ISO 3166-2 region
  code](https://en.wikipedia.org/wiki/ISO_3166-2)
* define a list of servers for Murakami to use for each test run
  * one test to a _randomly_ selected server in the list
  * one test to _all_ servers in the list
* multiple lists of servers are supported

You can review examples of the available options in:
`configs/ndt-custom-config.json.example`.

## DASH

The [DASH Streaming Test](https://ooni.org/nettest/dash/) test is designed to
measure the quality of tested networks by emulating a video streaming. This test
is called DASH because it uses the DASH ([Dynamic Adaptive Streaming over
HTTP](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP))
streaming technique.

## speedtest-cli

[speedtest-cli](https://github.com/sivel/speedtest-cli) is a community developed
command line program for testing the performance of a connection using the
speedtest.net platform. While this tool [does not claim parity with the official
test clients provided by
OOKLA](https://github.com/sivel/speedtest-cli#inconsistency) (for example in
measuring latency), our benchmark testing has found that it does provide similar
performance measurements to the official OOKLA command line and web-based tests.
speedtest-cli is also [openly
licensed](https://github.com/sivel/speedtest-cli/blob/master/LICENSE).

## OONI Probe

[OONI Probe](https://ooni.org/install/cli) provides a [suite of
measurements](https://ooni.org/nettest/) that can potentially serve as evidence
of Internet censorship since it shows how, when, where, and by whom it is
implemented. The Open [Observatory of Network Interference](https://ooni.org)
(OONI) is a non-profit free software project that aims to empower decentralized
efforts in documenting Internet censorship around the world.

Within Murakami, OONI Probe runs using the [unattended
option](https://ooni.org/support/ooni-probe-cli#ooniprobe-run-unattended), which
includes all tests except the DASH and NDT performance tests. For Murakami,
DASH and NDT are provided as separate runners. OONI Probe unattended
communicates with the OONI backend service to automate the targets of each test
depending on the current conditions of each probe.

### Potential Risks in Running OONI Probe

OONI Probe checks whether your provider blocks access to sites and services.
Running OONI Probe helps researchers collect evidence of internet censorship.

However, if your Murakami device will be run from locations where internet
censorship occurs or where repression and freedom of expression online is at
risk, this may also be a risk to you or those at the location where the device
is running tests.

Please, be aware that:
* Anyone monitoring your internet activity (such as your government or ISP) may
  be able to see that you are running OONI Probe.
* The network data you will collect will automatically be published (unless you
  opt-out in the settings).
* You may test objectionable sites.

Read the documentation to learn more: https://ooni.org/about/risks/

By enabling OONI Probe in Murakami, it is assumed you have read and understand
these risks and consent to help collect data on possible internet censorship.

## Output Specifications for Murkami Test Runners

### ndt5 Murakami JSON output specification
```
{
	"ServerName": "ndt-iupui-mlab1-iad03.measurement-lab.org",
	"ServerIP": "38.90.140.139"
	"ClientIP": "104.145.221.196",
	"MurakamiLocation": "<MURAKAMI 'LOCATION' ENV VAR>",
	"MurakamiNetworkType": "<MURAKAMI 'NETWORK_TYPE' ENV VAR>",
	"MurakamiConnectionType": "<MURAKAMI 'CONNECTION_TYPE' ENV VAR>",
	"TestUUID": "NULL",
        "TestProtocol": "ndt5",
        "TestError": "recvResultsAndLogout failed: cannot get message: read tcp 192.168.178.28:58788-\u003e77.67.115.11:3001: i/o timeout",
	"DownloadTestStartTime": "2020-02-18 20:32:52.639720903 +0000 UTC m=+5825.539350534",
	"DownloadTestEndTime": "2020-02-18 20:33:02.640686711 +0000 UTC m=+5835.540316330",
	"DownloadValue": "NULL", 
	"DownloadUnit": "Mbit/s", 
        "DownloadError": "download failed: cannot get TestPrepare message: read tcp 192.168.178.28:58788-\u003e77.67.115.11:3001: i/o timeout",
	"UploadValue": "NULL", 
	"UploadUnit": "Mbit/s", 
        "UploadError": "upload failed: cannot get TestMsg message: read tcp 192.168.178.28:58788-\u003e77.67.115.11:3001: i/o timeout",
	"DownloadRetransValue": "NULL", 
	"DownloadRetransUnit": "pct", 
	"MinRTTValue": "NULL",
	"MinRTTUnit": "ms"
}
```

### ndt7 Murakami JSON output specification

**Successful test:**
```
{
  "SchemaVersion": 1,
  "TestName": "ndt7",
  "TestStartTime": "2020-02-25T17:02:40.918022",
  "TestEndTime": "2020-02-25T17:03:01.754734",
  "MurakamiLocation": "Corciano",
  "MurakamiConnectionType": "wifi",
  "MurakamiNetworkType": "home",
  "ServerName": "ndt-iupui-mlab3-mil04.measurement-lab.org",
  "ServerIP": "213.242.77.165",
  "ClientIP": "93.188.101.116",
  "DownloadUUID": "ndt-cz99j_1580820576_000000000003708B",
  "DownloadValue": 405.32368416128276,
  "DownloadUnit": "Mbit/s",
  "DownloadError": null,
  "UploadValue": 26.85925099645699,
  "UploadUnit": "Mbit/s",
  "UploadError": null,
  "DownloadRetransValue": 2.3442441873334583,
  "DownloadRetransUnit": "%",
  "MinRTTValue": 29.108,
  "MinRTTUnit": "ms"
}
```

**Failed Test:**
```
{
  "SchemaVersion": 1,
  "TestName": "ndt7",
  "TestStartTime": "2020-02-21T14:45:05.960649",
  "TestEndTime": "2020-02-21T14:45:05.965838",
  "MurakamiLocation": "Corciano",
  "MurakamiConnectionType": "wifi",
  "MurakamiNetworkType": "home",
  "DownloadError": "Get https://locate.measurementlab.net/ndt7: dial tcp: lookup locate.measurementlab.net: Temporary failure in name resolution",
  "UploadError": "Get https://locate.measurementlab.net/ndt7: dial tcp: lookup locate.measurementlab.net: Temporary failure in name resolution",
  "ServerName": null,
  "ServerIP": null,
  "ClientIP": null,
  "DownloadUUID": null,
  "DownloadValue": null,
  "DownloadUnit": null,
  "UploadValue": null,
  "UploadUnit": null,
  "DownloadRetransValue": null,
  "DownloadRetransUnit": null,
  "MinRTTValue": null,
  "MinRTTUnit": null
}
```

### DASH Murakami JSON output specification
```
{
    "ServerIP": "194.116.85.211",
    "ClientIP": "79.40.147.190",
    "MurakamiLocation": "<MURAKAMI 'LOCATION' ENV VAR>",
    "MurakamiNetworkType": "<MURAKAMI 'NETWORK_TYPE' ENV VAR>",
    "MurakamiConnectionType": "<MURAKAMI 'CONNECTION_TYPE' ENV VAR>",    
    "TestUUID": "4364c5da-a07b-4188-9cbd-ad79e5a7c2f8",   
    "TestProtocol": "dash",
    "TestError": "NULL",
    "TestRuntime": 33.1672148704529,
    "TestRuntimeUnits": "seconds",
    "TestStartTime": "2017-07-24 09:44:53",
    "ProbeASN": "AS1234",
    "ProbeCC": "IT",
    "ConnectLatency": 0.0268912315368652,
    "ConnectLatencyUnits": "seconds" 
    "MedianBitrate": 5786.0,
    "MedianBitrateUnits": "Kbit/s",
    "MinPlayoutDelay": 0.214933633804321
    "MinPlayoutDelayUnits": "seconds"
}
```

### speedtest-cli Murakami JSON output specification
```
{
  "TestName": "speedtest-cli-multi-stream",
  "TestStartTime": "2020-02-26T17:31:09.294212",
  "TestEndTime": "2020-02-26T17:31:32.438628",
  "MurakamiLocation": "<MURAKAMI 'LOCATION' ENV VAR>",
  "MurakamiNetworkType": "<MURAKAMI 'NETWORK_TYPE' ENV VAR>",
  "MurakamiConnectionType": "<MURAKAMI 'CONNECTION_TYPE' ENV VAR>",   
  "Download": 205429128.65829697,
  "DownloadUnits": "Bit/s",
  "Upload": 62332520.98624364,
  "UploadUnits": "Bit/s",
  "Ping": 20.556,
  "PingUnits": "ms",
  "BytesSent": 78004224,
  "BytesReceived": 258037852,
  "Share": null,
  "Timestamp": "2020-02-26T17:31:09.912341Z",
  "ServerURL": "http://speedtest.netandwork.net:8080/speedtest/upload.php",
  "ServerLat": "44.7709",
  "ServerLon": "10.7819",
  "ServerName": "Correggio",
  "ServerCountry": "Italy",
  "ServerCountryCode": "IT",
  "ServerSponsor": "NETandWORK s.r.l.",
  "ServerID": "20372",
  "ServerHost": "speedtest.netandwork.net:8080",
  "ServerDistance": 53.7642143944149,
  "ServerLatency": 20.556,
  "ServerLatencyUnits": "ms",
  "ClientIP": "93.188.101.116",
  "ClientLat": "44.4938",
  "ClientLon": "11.3387",
  "Isp": "Ehinet Srl",
  "IspRating": "3.7",
  "Rating": "0",
  "IspDownloadAvg": "0",
  "IspUploadAvg": "0",
  "LoggedIn": "0",
  "Country": "IT"
}
```

### OONI Probe Murakami JSON output specification

```
{
  "TestName": "ooniprobe-middlebox",
  "TestStartTime": "2021-11-11T17:33:24.105157",
  "TestEndTime": "2021-11-11T17:44:16.477665",
  "MurakamiLocation": null,
  "MurakamiConnectionType": null,
  "MurakamiNetworkType": null,
  "MurakamiDeviceID": "",
  "TestResults": [
    {
      "fields": {
        "asn": 43989,
        "failure_msg": "",
        "id": 1,
        "is_anomaly": false,
        "is_done": true,
        "is_failed": false,
        "is_first": true,
        "is_last": false,
        "is_upload_failed": false,
        "is_uploaded": true,
        "measurement_file_path": "/home/roberto/.ooniprobe/msmts/middlebox-2021-11-11T173329.262160187Z/msmt-http_invalid_request_line-0.json",
        "network_country_code": "IT",
        "network_name": "Ehinet Srl",
        "report_file_path": "",
        "runtime": 5.386668622,
        "start_time": "2021-11-11T17:33:29.431065843Z",
        "test_group_name": "middlebox",
        "test_keys": "{}",
        "test_name": "http_invalid_request_line",
        "type": "measurement_item",
        "upload_failure_msg": "",
        "url": "",
        "url_category_code": "",
        "url_country_code": ""
      },
      "level": "info",
      "timestamp": "2021-11-11T18:44:16.510108991+01:00",
      "message": "measurement"
    },
    {
      "fields": {
        "asn": 43989,
        "failure_msg": "",
        "id": 2,
        "is_anomaly": false,
        "is_done": true,
        "is_failed": false,
        "is_first": false,
        "is_last": true,
        "is_upload_failed": false,
        "is_uploaded": true,
        "measurement_file_path": "/home/roberto/.ooniprobe/msmts/middlebox-2021-11-11T173329.262160187Z/msmt-http_header_field_manipulation-0.json",
        "network_country_code": "IT",
        "network_name": "Ehinet Srl",
        "report_file_path": "",
        "runtime": 0.561414746,
        "start_time": "2021-11-11T17:33:35.006617306Z",
        "test_group_name": "middlebox",
        "test_keys": "{}",
        "test_name": "http_header_field_manipulation",
        "type": "measurement_item",
        "upload_failure_msg": "",
        "url": "",
        "url_category_code": "",
        "url_country_code": ""
      },
      "level": "info",
      "timestamp": "2021-11-11T18:44:16.510207101+01:00",
      "message": "measurement"
    }
  ]
}
```
