# Builder image
FROM alpine:3.9 as build
MAINTAINER Measurement Lab Support <support@measurementlab.net>

RUN apk add --update build-base gcc cmake libressl-dev curl-dev git

# Install libndt
# TODO: Use an actual release tag. This commit is currently the latest one
# on the release/v0.27.0 branch, including the fix to make libndt build with
# musl-libc. It needs to be updated when v0.27.0 is released.
RUN git clone https://github.com/measurement-kit/libndt.git
WORKDIR /libndt
RUN git checkout 41e93c6a64684603e76ef686197877c749ae9c98

RUN cmake .
RUN cmake --build . -j $(nproc)
# RUN ctest -a --output-on-failure .

# Install dash
WORKDIR /
FROM golang:1.13.0-alpine3.10
RUN apk add git
RUN git clone https://github.com/neubot/dash.git
WORKDIR /dash
RUN git checkout 176e7b5825c6c5c7a8840c460eccee60e01a097b

RUN build.sh

FROM gcr.io/distroless/static@sha256:9b60270ec0991bc4f14bda475e8cae75594d8197d0ae58576ace84694aa75d7a
COPY --from=build /go/bin/dash-server /
EXPOSE 80/tcp 443/tcp
WORKDIR /
ENTRYPOINT ["/dash-server"]

RUN rm -f ./certs/*.pem &&                     \
  ./mkcerts.bash &&                            \
  sudo chown root:root ./certs/*.pem &&        \
  docker run --network=bridge                  \
             --publish=80:8888                 \
             --publish=443:4444                \
             --publish=9990:9999               \
             --volume `pwd`/certs:/certs:ro    \
             --volume `pwd`/datadir:/datadir   \
             --read-only                       \
             --cap-drop=all                    \
             neubot/dash                       \
             -datadir /datadir                 \
             -http-listen-address :8888        \
             -https-listen-address :4444       \
             -prometheusx.listen-address :9999 \
             -tls-cert /certs/cert.pem         \
             -tls-key /certs/key.pem

FROM python:3-alpine3.9
RUN apk add git

# Install speedtest-cli
RUN pip install speedtest-cli

# Murakami image
RUN pip install 'poetry==0.12.17'

WORKDIR /murakami
COPY poetry.lock pyproject.toml /murakami/

# Set up poetry to not create a virtualenv, since the docker container is
# isolated already, and install the required dependencies.
RUN poetry config settings.virtualenvs.create false \
    && poetry install --no-dev --no-interaction

# Copy Murakami and previously built test clients into the container.
COPY . /murakami/
COPY --from=build /libndt/libndt-client /murakami/bin/

CMD python -m murakami
