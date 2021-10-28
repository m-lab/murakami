# Build ndt7, ndt5 and dash Go clients.
FROM golang:1.17-bullseye AS build
RUN apt-get update
RUN apt-get install -y git
ENV GO111MODULE=on
RUN go get github.com/neubot/dash/cmd/dash-client@master
RUN go get github.com/m-lab/ndt7-client-go/cmd/ndt7-client
RUN go get github.com/m-lab/ndt5-client-go/cmd/ndt5-client

# Murakami image
FROM python:3.7-bullseye
# Install dependencies and speedtest-cli
RUN apt-get update
RUN apt-get install -y git gcc libc-dev libffi-dev libssl-dev make rustc cargo
RUN /usr/local/bin/python3.7 -m pip install --upgrade pip
RUN pip install -e git://github.com/sivel/speedtest-cli.git@v2.1.3#egg=speedtest-cli
RUN pip install 'poetry==1.1.7'

WORKDIR /murakami

# Copy Murakami and previously built test clients into the container.
COPY . /murakami/
COPY --from=build /go/bin/* /murakami/bin/

# Set up poetry to not create a virtualenv, since the docker container is
# isolated already, and install the required dependencies.
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction

# Add binaries' path to PATH.
ENV PATH="/murakami/bin:${PATH}"

ENTRYPOINT [ "python", "-m", "murakami" ]
