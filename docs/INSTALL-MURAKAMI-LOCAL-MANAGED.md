# Installation and Use - Murakami Container on Standalone Devices, Managed by a Mozilla WebThings Gateway

Murakami Standalone installed devices can be managed using a [Mozilla WebThings Gateway](https://iot.mozilla.org/gateway/). Using the gateway allows you to manage the configuration and data for one or more Murakami devices from the WebThings Gateway, which also provides remote access when you're somewhere other than the network where your Murakami devices are placed.

Follow the [instructions on Mozilla's site](https://iot.mozilla.org/gateway/) to setup a WebThings Gateway on the network where you wish to place Murakami measurement devices. If you prefer not to use a Raspberry Pi or Turris Omnia, which are the Gateways they have instructions for, you can build from scratch following the [instructions here](https://github.com/mozilla-iot/gateway).

## Installing Murakami

Installing Murakami is the same in this situation as the [standalone installation](INSTALL-MURAKAMI-STANDALONE.md). Once your device is running a Murakami container, your WebThings Gateway should be able to detect and configure it.

## Configuring Murakami Devices Via a WebThings Gateway

Once you have a WebThings Gateway and at least one Murakami container running on the same network, log into your WebThings Gateway to add each container as a "M-Lab Murakami WebThing." You'll need to know the hostname or IP address for each Murakami container.

On the "Things" page of the WebThings Gateway, click the + icon in the lower right corner of the page to add a new Thing.
![Add WebThing Icon](images/webthing_add_icon.png)

The Gateway will begin scanning for new devices. Click "Add by URL..."
![Add by URL image](images/webthing_add_by_url.png)

Enter the IP address of the computer that is running the Murakami container and press "Submit".
![Add by URL entry screen](images/webthing_enter_hostname_ip.png)

Name your Murakami WebThing and leave “NetworkTest” selected in the drop down menu, then click save. Once the message “Saved” appears, click “Done”.
![Name and Save Murakami WebThing image](images/webthing_name_murakami.png)

The Murakami WebThing now appears in your list of Things.
![Murakami WebThing image](images/webthing_listed.png)

Click on the small bubble in the upper right to access the Murakami WebThings settings. The settings page displays all available test runners enabled in the Murakami container, and allows you to toggle each on or off.
![Murakami WebThing Setting image](images/webthing_settings.png)
