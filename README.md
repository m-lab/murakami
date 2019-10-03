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

### setup for building for different arch targets locally

- apt install qemu-user
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker run --rm -t arm64v8/ubuntu uname -m
###which should display aarch64 (meaning you're running an arm64 container)
- edit .docker/config.json
	{    
        "experimental": "enabled"    
	}    
- docker buildx create --name arm --platform "linux/arm/v7,linux/arm64"
- docker buildx inspect arm --bootstrap
- docker buildx use arm

### Build an image for armv7

docker buildx build --platform "linux/arm/7" -t murakami:latest --load .

### Push image to dockerhub

$ docker buildx build --platform "linux/arm/7" -t murakami:latest --push  .

### Run standalone container on localhost
$ docker run -e "MURAKAMI_EXPORTERS_LOCALHOST_TYPE=local" -e "MURAKAMI_EXPORTERS_LOCALHOST_ENABLED=true" --volume /root/data:/var/cache/murakami/ critzo/murakami:armv7-latest  --immediate


### Configuring the Murakami Test Runners & Storage Options


### Running a Murakami Test Manually

* 
poetry run murakami --help