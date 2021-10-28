# Optional - Using the Murakami-Viz Web Service with Murakami Measurement Devices

[Murakami-Viz](https://github.com/m-lab/murakami-viz/) was developed in collaboration with US public libraries, Simmons University, and Internet2's Community Anchor program, as an accompanying service to Murakami, with support from the Institute for Museum and Library Services (IMLS) in IMLS Award [#LG-71-18-0110-18](https://www.imls.gov/grants/awarded/lg-71-18-0110-18). The application is a Docker-based web service that provides a basic data visualization and access service for tests collected by Murakami measurement devices. Though it's initial audience and user interfaces are somewhat public library focused, Murakami-Viz can be useful for any organization as a part of their measurement initiatives.

## Installation

Please follow the instructions in the [Murakami-Viz README](https://github.com/m-lab/murakami-viz/blob/master/README.md).

## Configuring Murakami Measurement Devices to Send Result to Murakami-Viz

The HTTP exporter is provided in Murakami, to enable test results to be sent to your Murakami-Viz server. Like other configurations for Murakami, this is done using environment variables.

Three environment variables enable all test results to be sent to your Murakami-Viz service:

```
MURAKAMI_EXPORTERS_HTTP0_TYPE = http
MURAKAMI_EXPORTERS_HTTP0_ENABLED = 1
MURAKAMI_EXPORTERS_HTTP0_URL = "<url or IP address>/api/v1/runs"
```

For standalone Murakami devices, these variables should be defined for every device that should send data to the service. For Balena.io managed devices, you can define these as application level variables.

## Configuring Murakami-Viz to Receive Test Results

For each Murakami device that will send test data to Murakami-Viz, you must define that device manually in the Murakami-Viz service, and add the public IP address(es) from which Murakami devices will send test results. If your Murakami device is on a connection that doesn't have a static IP, you may wish to periodically export or upload test data to Murakami-Viz using the included [upload utility](UPLOAD-UTILITY.md) instead. See [configuring Murakami-Viz](https://github.com/m-lab/murakami-viz/blob/master/README.md#post-install-configuration) for complete setup details.
