# Murakami Supported Test Runners

## What is a "Runner"?

Murakami provides a collection of _runners_, which are script wrappers around
external measurement tools. Each of these tools runs some sort of internet
measurement. To add new measurement tools to Murakami, please see [Adding New
Test Runners](ADDING-NEW-TEST-RUNNERS.md)

## Sample Output for All Murkami Test Runners

* [dash-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl](example-test-output/dash-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl)
* [ndt5-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl](example-test-output/ndt5-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl)
* [ndt7-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl](example-test-output/ndt7-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl)
* [ooniprobe-circumvention-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl](example-test-output/ooniprobe-circumvention-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl)
* [ooniprobe-im-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl](example-test-output/ooniprobe-im-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl)
* [ooniprobe-middlebox-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl](example-test-output/ooniprobe-middlebox-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl)
* [ooniprobe-websites-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl](example-test-output/ooniprobe-websites-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl)
* [ookla-speedtest-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime.jsonl](example-test-output/ookla-speedtest-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-test_datetime)

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
based on the geolocation of the client IP address.

The `ndt5custom` and `ndt7custom` runners provide additional capabilities:

* run tests to self-hosted ndt-servers
* use the M-Lab Locate Service to [select servers](https://github.com/m-lab/locate/blob/master/USAGE.md#how-gcp-identifies-client-location) by I[SO 3166-1 alpha 2 country
  code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) or [ISO 3166-2 region
  code](https://en.wikipedia.org/wiki/ISO_3166-2)
* define a list of servers for Murakami to use for each test run
  * one test to a _randomly_ selected server in the list
  * one test to _all_ servers in the list
* multiple lists of servers are supported

The configuration file `configs/ndt-custom-config.json.example` is provided as a
starting point. Below are the contents of the example file, followed by
additional details for using the available options.

```
{
    "regions": [ "CA-ON", "CA-BC", "CA-AB" ],
    "countries": [ "GB", "KE", "MG" ],
    "serverGroups": [
        {
            "selection": "all",
            "servers": [
                "10.10.20.15:8080"
            ]
        },
        {
            "selection": "random",
            "servers": [
                "localhost"
            ]
        }
    ]
}
```

### Selecting Multiple M-Lab Servers by Region Code

`"regions": [ "CA-ON", "CA-BC", "CA-AB" ],` 
Selects three M-Lab servers in Ontario, Brittish Columbia, and Alerta, Canada.
Any valid ISO 3166-2 region code is valid.

### Selecting Multiple M-Lab Servers by Country Code

`"countries": [ "GB", "KE", "MG" ],`
Selects three M-Lab servers in Great Brittain, Kenya, and Madagascar. Any valid
ISO 3166-1 country code is valid.

### Defining Custom Server Groups and Selection Strategies

The `ServerGroups` section demonstrates how to define custom lists of M-Lab or
self-provisioned ndt-servers for your Murakami device to use for NDT tests. Each
group of servers can use either the `random` or `all` selection strategy.
`random` selects one server for each test run, and `all` will instruct Murakami
to run one test to all servers in the list during each test run. Servers are
defined as either IP addresses or fully qualified domain names of
M-Lab or self-provisioned servers. In the example above, the IP address of a
self-provisioned ndt-server running in a local area network is defined, but a
public IP address is also valid.

### Output Files for Custom NDT Runners

The output files of both NDT custom runners is the same as the non-custom
runners, except an index number is defined in each test result when multiple
servers are defined in `ndt-custom-config.json`. For example, when using the
example as is for the ndt7custom runner, seven ndt7 tests are conducted for each
Murakami test run, indexed with 0-6:

* ndt7custom-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-**0**-2021-11-19T12:16:19.356279.jsonl
* ndt7custom-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-**1**-2021-11-19T12:16:19.356279.jsonl
* ndt7custom-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-**2**-2021-11-19T12:16:19.356279.jsonl
* ndt7custom-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-**3**-2021-11-19T12:16:19.356279.jsonl
* ndt7custom-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-**4**-2021-11-19T12:16:19.356279.jsonl
* ndt7custom-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-**5**-2021-11-19T12:16:19.356279.jsonl
* ndt7custom-_LOCATION-_NETWORK_TYPE-_CONNECTION_TYPE-**6**-2021-11-19T12:16:19.356279.jsonl

## DASH

The [DASH Streaming Test](https://ooni.org/nettest/dash/) test is designed to
measure the quality of tested networks by emulating a video streaming. This test
is called DASH because it uses the DASH ([Dynamic Adaptive Streaming over
HTTP](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP))
streaming technique.

## Ookla Speedtest

[ookla-speedtest](https://www.speedtest.net/apps/cli) is the official command
line client test published by Ookla.

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

Within Murakami, OONI Probe runs with the [unattended
option](https://ooni.org/support/ooni-probe-cli#ooniprobe-run-unattended), which
includes [four tests](https://ooni.org/support/ooni-probe-cli#ooniprobe-run):

* circumvention
* im
* middlebox
* websites

If your Murakami device will be run from locations where internet censorship
occurs or where repression and freedom of expression online is at risk, this may
also be a risk to you or those at the location where the device is running tests.

Please, be aware that:
* Anyone monitoring your internet activity (such as your government or ISP) may
  be able to see that you are running OONI Probe.
* The network data you will collect will automatically be published (unless you
  opt-out in the settings).
* You may test objectionable sites.

Read the documentation to learn more: https://ooni.org/about/risks/

By enabling OONI Probe in Murakami, it is assumed you have read and understand
these risks and consent to help collect data on possible internet censorship.
