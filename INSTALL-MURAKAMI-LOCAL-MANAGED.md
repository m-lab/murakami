# Installation and Use - Murakami Container on Standalone Devices, Managed by a Mozilla WebThings Gateway

Murakami Standalone installed devices can be managed using a [Mozilla WebThings Gateway](https://iot.mozilla.org/gateway/). Using the gateway allows you to manage the configuration and data for one or more Murakami devices from the WebThings Gateway, which also provides remote access when you're somewhere other than the network where your Murakami devices are placed.

Follow the [instructions on Mozilla's site](https://iot.mozilla.org/gateway/) to setup a WebThings Gateway on the network where you wish to place Murakami measurement devices. If you prefer not to use a Raspberry Pi or Turris Omnia, which are the Gateways they have instructions for, you can build from scratch following the [instructions here](https://github.com/mozilla-iot/gateway).

## Installing Murakami

Installing Murakami is the same in this situation as the [standalone installation](INSTALL-MURAKAMI-STANDALONE.md). Once your device is running a Murakami container, your WebThings Gateway should be able to detect and configure it.

## Configuring Murakami Devices Via a WebThings Gateway

**TO DO:** Add instructions.
