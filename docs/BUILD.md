# Building Murakami Container Images

This document provides a guide on how to build your own Murakami container
images, instead of running those provided by M-Lab. Developers and project
contributors may wish to do this to build support for new system architectures,
or to test development of new features locally.

## Configuring Your System to Build Images for Different System Architectures

Development systems may vary in system architecture, thus we recommend using the
qemu-user package to allow you to build for other system types. The following
outlines how to add support for building armv7hf and armv8/aarch64 images. We
assume that you already have Docker running on your development system.

Run each of the the following lines one at a time in your terminal:
```
sudo apt install qemu-user
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker run --rm -t arm64v8/ubuntu uname -m
```

After running the last command, `aarch64` should be displayed, meaning you're running an arm64 container.

Edit `.docker/config.json`, adding the following section:
```	
	{    
        "experimental": "enabled"    
	}
```

Add support for the `armv7hf` system architecture:
```
docker buildx create --name arm --platform "linux/arm/v7,linux/arm64"
docker buildx use arm
```

You should now be able to build for the following system architectures:
```
linux/arm/v7, linux/arm64, linux/amd64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v6
```

Use this command to show which arm platforms are supported:
```docker buildx inspect arm --bootstrap```

## Clone Murakami and Build Images

```
git clone https://github.com/m-lab/murakami.git && cd murakami

# Build for armv7hf:

docker buildx build --platform "linux/arm/7" -t <your dockerhub>/murakami:<desired tag> --load .

# Build for armv8/aarch64:>

docker buildx build --platform "linux/arm64" -t <your dockerhub>/murakami:<desired tag> --load .
```

### Push an Image to Dockerhub

```
docker buildx build --platform "linux/arm/7" -t <your dockerhub>/murakami:<desired tag> --push .
```
