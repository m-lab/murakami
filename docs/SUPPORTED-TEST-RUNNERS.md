# Murakami Supported Test Runners

## NDT

The [Network Diagnostic Tool (NDT)](https://www.measurementlab.net/tests/ndt/) from M-Lab is a single stream performance measurement of a connection’s capacity for “bulk transport” (as defined in IETF’s [RFC 3148](https://tools.ietf.org/html/rfc3148). NDT measures “single stream performance” or “bulk transport capacity”. NDT reports upload and download speeds and latency metrics.

M-Lab provides two NDT protocols, [ndt5](https://www.measurementlab.net/tests/ndt/ndt5) and [ndt7](https://www.measurementlab.net/tests/ndt/ndt7).

### NDT 5 

Murakami includes M-Lab's [NDT 5 Go client](https://github.com/m-lab/ndt5-client-go). NDT 5 is the legacy protocol, measuring a connection's performance using the TCP CUBIC and TCP RENO compression algorithms. NDT 5 requires a specific set of [network ports](https://www.measurementlab.net/faq/#what-firewall-ports-does-ndt-require-to-be-open) to be open in order to run. M-Lab will eventually deprecate the NDT5 protocol once the NDT7 protocol is adopted and in wider use.

### NDT 7

Murakami includes M-Lab's [NDT 7 Go client](https://github.com/m-lab/ndt7-client-go). The [NDT 7 protocol](https://github.com/m-lab/ndt-server/blob/master/spec/ndt7-protocol.md) measures a connection's performance using TCP BBR in networks supporting it. NDT 7 operates solely on port 443 and provides a better end-to-end measurement than past NDT versions.

## DASH

The [DASH Streaming Test](https://ooni.org/nettest/dash/) test is designed to measure the quality of tested networks by emulating a video streaming. This test is called DASH because it uses the DASH ([Dynamic Adaptive Streaming over HTTP](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)) streaming technique.\

## speedtest-cli

[speedtest-cli](https://github.com/sivel/speedtest-cli) is a community developed command line program for testing the performance of a connection using the speedtest.net platform. While this tool [does not claim parity with the official test clients provided by OOKLA](https://github.com/sivel/speedtest-cli#inconsistency) (for example in measuring latency), our benchmark testing has found that it does provide similar performance measurements to the official OOKLA command line and web-based tests. speedtest-cli is also [openly licensed](https://github.com/sivel/speedtest-cli/blob/master/LICENSE).

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
