# murakami
A new version of the M-Lab Murakami network measurement tap.


## Setup for Balena Cloud Managed Murakami Deployment

### Configuring Murakami Test Runners & Storage Options

### Running a Murakami Test Manually

Connect to the running Balena cloud managed device container, either through the Balena web UI or balena cli tool:

* ndt7: `bin/libndt-client --ndt7 -download -upload`
* ndt: `bin/libndt-client -download -upload`
* saving results locally: `bin/libndt-client --ndt7 -download -upload -batch 1> /data/test-ndt7.json`



## Setup for Standalone or WebThings Gateway Managed Murakami Measurement Devices 

### Install the Host OS

We recommend using a recent Linux OS image provided by Hardkernel:

* odroid-xu4 - https://wiki.odroid.com/odroid-xu4/os_images/linux/start
* odroid-c2 - https://wiki.odroid.com/odroid-c2/os_images/ubuntu/ubuntu
* odroid-c1 - https://wiki.odroid.com/odroid-c1/os_images/ubuntu/ubuntu
* odroid-n2 - https://wiki.odroid.com/odroid-n2/os_images/ubuntu

If using a WiFi connection and the Ubuntu minimal images, the utility `nmtui` is one way to connect and save the WiFi connection.

### Install Docker

### Build Murakami Docker image or Pull from Dockerhub

* `git clone ...`
* `docker build -t murakami:latest .`
* docker run measurementlab/murakami:TAG
* docker run evfirerob/murakami:latest

### Create a folder to store your test results

* `mkdir data/`
                           --settings.path=/data
### Pull and Run the Murakami Docker Container

# map data/ on the host to /data in the container
* `docker run murakami:latest --volume `pwd`/data:/data --settings.path=/data`  


### Configuring the Murakami Test Runners & Storage Options


### Running a Murakami Test Manually

* 
