#!/bin/bash
## Balena fleet device provisioning script
##
## This script can be used to provision new devices in your fleet. 
## Requires balena-cli to be installed, and authorized. 
## See: https://github.com/balena-io/balena-cli/
##

usage="$0 <balena fleet name> <MURAKAMI_LOCATION> <MURAKAMI_CONNECTION_TYPE> <MURAKAMI_NETWORK_TYPE>"
balenaFleet=${1:?Please provide the Balena fleet name: ${usage}}
loc=${2:?Please provide the MURAKAMI_LOCATION for this device: ${usage}}
conn=${3:?Please provide the MURAKAMI_CONNECTION_TYPE for this device: ${usage}}
net=${4:?Please provide the MURAKAMI_NETWORK_TYPE for this device: ${usage}}

## register new device
uuid=$(balena device register $balenaFleet | awk '{ print $4 }')

## construct a unique but recognizable device name
deviceName="${uuid}"

# rename the device
balena device rename ${uuid} ${deviceName}

# set device environment variables used by Murakami
balena env add MURAKAMI_LOCATION ${loc} --device ${uuid}
balena env add MURAKAMI_CONNECTION_TYPE ${conn} --device ${uuid}
balena env add MURAKAMI_NETWORK_TYPE ${net} --device ${uuid}

# let us know the operation was completed
echo "added $deviceName to $balenaFleet"

# Download an SD card image
balena os download odroid-xu4 -o $balenaFleet.img --version latest

# Generate a config for this device to be injected on a freshly flashed
# SD card.
balena config generate --device ${uuid} --version 2.38.3+rev3 --network ethernet --appUpdatePollInterval 10 --output balenaDeviceConfigs/${uuid}_config.json

echo ""
echo "${deviceName} has been registered in ${balenaFleet}."
echo "Next, complete the provisioning of this device by:"
echo ""
echo "  * Write the OS image below to an SD card:"
echo "    ${balenaFleet}.img"
echo "  * Then, with the SD card still inserted, run the command below"
echo "    to add the device's configuration:"
echo "    balena config inject balenaDeviceConfigs/${uuid}_config.json --type odroid-xu4 --drive /your/sdcard/disk"
echo ""
echo "Note: substitute the drive path for your SD card for '/your/sdcard/disk' in the command above."
