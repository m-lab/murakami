# Builder image
FROM python:3-alpine3.10 AS build
MAINTAINER Measurement Lab Support <support@measurementlab.net>

RUN apk add --update build-base gcc cmake libressl-dev curl-dev git linux-headers

# Download and build libndt.
RUN git clone https://github.com/measurement-kit/libndt.git
WORKDIR /libndt

RUN cmake .
RUN cmake --build . -j $(nproc)

# Build dash-client
FROM golang:1.13.0-alpine3.10 AS dashbuild
RUN apk add --no-cache git
RUN go get github.com/neubot/dash/cmd/dash-client

# Murakami image
FROM python:3-alpine3.10
RUN apk update && apk upgrade
# Install dependencies and speedtest-cli
RUN apk add git curl libstdc++ libgcc gcc libc-dev libffi-dev libressl-dev speedtest-cli make
RUN pip install 'poetry==0.12.17'

WORKDIR /murakami

# Install gcloud SDK so we can use gsutil.
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# Copy Murakami and previously built test clients into the container.
COPY . /murakami/
COPY --from=build /libndt/libndt-client /murakami/bin/
COPY --from=dashbuild /go/bin/dash-client /murakami/bin/

# Set up poetry to not create a virtualenv, since the docker container is
# isolated already, and install the required dependencies.
RUN poetry config settings.virtualenvs.create false \
    && poetry install --no-dev --no-interaction --develop=murakami

# Add binaries' path to PATH.
ENV PATH="/murakami/bin:${PATH}"

ENTRYPOINT [ "/usr/local/bin/poetry", "run", "murakami" ]
