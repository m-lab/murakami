#!/bin/bash
set -euo pipefail

## Balena fleet device provisioning script
##
## This script can be used to provision new devices in your fleet. 
## Requires balena-cli to be installed, and authorized. 
## See: https://github.com/balena-io/balena-cli/
##

# First check to confirm balena-cli is installed
balenaInstalled=$(which balena || true )

if [ -z ${balenaInstalled} ]; then
	echo "balena-cli is not installed on this system."
	echo "See: https://github.com/balena-io/balena-cli/"
	exit 1
fi
echo "balena is installed at: ${balenaInstalled}"

# Also check that the user is logged in
if ! balena fleets; then exit 1; fi

usage="$0 <balena fleet name> <MURAKAMI_NETWORK_TYPE> <MURAKAMI_CONNECTION_TYPE>"
balenaFleet=${1:?Please provide the Balena fleet name: ${usage}}
net=${2:?Please provide the ISP Name for this device without spaces (e.g. IspName, Isp-Name, Isp_Name): ${usage}}
conn=${3:?Please provide the ISP Plan for this device without spaces (e.g. PlanName, 10_4, 25_3): ${usage}}

## register new device
uuid=$(balena device register $balenaFleet | awk '{ print $4 }')

## construct a unique but recognizable device name
deviceName="${uuid}"

# rename the device
balena device rename ${uuid} ${deviceName}

# set device environment variables used by Murakami
balena env add MURAKAMI_SETTINGS_LOCATION ${deviceName} --device ${uuid}
balena env add MURAKAMI_SETTINGS_NETWORK_TYPE ${net} --device ${uuid}
balena env add MURAKAMI_SETTINGS_CONNECTION_TYPE ${conn} --device ${uuid}

# let us know the operation was completed
echo "added $deviceName to $balenaFleet"

# Download an SD card image
balenaDeviceType=$(balena fleet $balenaFleet | grep 'DEVICE TYPE' | cut -f 1 | cut -d ":" -f2 )

echo "Enter 'Y' if you need to download the latest release image? Press any other key to continue."
read downloadDeviceImage

if [ ${downloadDeviceImage} = "Y"  ]; then
	balena os download $balenaDeviceType -o $balenaFleet.img --version latest
fi

# Generate a config for this device to be injected on a freshly flashed
# SD card. Version in this case refers to the Balena host OS version.
balena config generate --device ${uuid} --version 2.38.3+rev3 --network ethernet --appUpdatePollInterval 10 --output balenaDeviceConfigs/${uuid}_config.json

availableDevice=$(balena util available-drives)

echo ""
echo "${deviceName} has been registered in ${balenaFleet}."
echo ""
echo "Next, complete the provisioning of this device:"
echo ""
echo "  * Write the OS image below to an SD card using Etcher or other utility:"
echo "    ${balenaFleet}.img"
echo ""
echo "  * Eject, then re-insert the SD card, and run the command below to add"
echo "    the device's configuration:"
echo ""
echo "    sudo balena config inject balenaDeviceConfigs/${uuid}_config.json --type odroid-xu4 --drive /your/sdcard/disk"
echo ""
echo "Substitute the drive or device path to your SD card for: "
echo "     '/your/sdcard/disk' in the command above."
echo ""
if [ -n "${availableDevice}" ]; then 
	echo "Your system has this device available: "
	echo "${availableDevice} "
	echo ""
	echo "Confirm this is the right device before using it!"
fi
echo ""
echo "  * Label the device. Repeat as needed."
echo ""
