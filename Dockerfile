# Builder image
FROM python:3-alpine3.10 AS build
MAINTAINER Measurement Lab Support <support@measurementlab.net>

RUN apk add --update build-base gcc cmake libressl-dev curl-dev git linux-headers

# Install libndt
# TODO: Use an actual release tag. This commit is currently the latest one
# on the release/v0.27.0 branch, including the fix to make libndt build with
# musl-libc. It needs to be updated when v0.27.0 is released.
RUN git clone https://github.com/measurement-kit/libndt.git
WORKDIR /libndt

RUN cmake .
RUN cmake --build . -j $(nproc)

# Install Dash
WORKDIR /
RUN git clone https://github.com/neubot/dash.git

FROM golang:1.13.0-alpine3.10 AS dashbuild
RUN apk add --no-cache git
COPY --from=build /dash /go/src/github.com/neubot/dash
WORKDIR /go/src/github.com/neubot/dash
RUN ./build.sh

FROM gcr.io/distroless/static@sha256:9b60270ec0991bc4f14bda475e8cae75594d8197d0ae58576ace84694aa75d7a
COPY --from=dashbuild /go/bin/dash-server /
EXPOSE 80/tcp 443/tcp
WORKDIR /
ENTRYPOINT ["/dash-server"]

# Murakami image and install speedtest-cli
FROM python:3-alpine3.10
RUN apk update && apk upgrade
RUN apk add git curl libstdc++ libgcc gcc libc-dev libffi-dev libressl-dev speedtest-cli make
RUN pip install 'poetry==0.12.17'

WORKDIR /murakami
COPY poetry.lock pyproject.toml /murakami/

# Set up poetry to not create a virtualenv, since the docker container is
# isolated already, and install the required dependencies.
RUN poetry config settings.virtualenvs.create false \
    && poetry install --no-dev --no-interaction

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

# Add binaries' path to PATH.
ENV PATH="/murakami/bin:${PATH}"

CMD python -m murakami -c /murakami/murakami.toml
