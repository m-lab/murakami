# Build ndt7, ndt5 and dash Go clients.
FROM golang:1.13.0-alpine3.10 AS build
RUN apk add --no-cache git
RUN go get github.com/m-lab/dash/cmd/dash-client
RUN go get github.com/m-lab/ndt7-client-go/cmd/ndt7-client
RUN go get github.com/m-lab/ndt5-client-go/cmd/ndt5-client

# Murakami image
FROM python:3-alpine3.10
RUN apk update && apk upgrade
# Install dependencies and speedtest-cli
RUN apk add git libgcc gcc libc-dev libffi-dev libressl-dev speedtest-cli make
RUN pip install 'poetry==0.12.17'

WORKDIR /murakami

# Copy Murakami and previously built test clients into the container.
COPY . /murakami/
COPY --from=build /go/bin/* /murakami/bin/

# Set up poetry to not create a virtualenv, since the docker container is
# isolated already, and install the required dependencies.
RUN poetry config settings.virtualenvs.create false \
    && poetry install --no-dev --no-interaction --develop=murakami

# Add binaries' path to PATH.
ENV PATH="/murakami/bin:${PATH}"

ENTRYPOINT [ "python", "-m", "murakami" ]
