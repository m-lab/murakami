# Builder image
FROM alpine:3.10.2 as build
MAINTAINER Measurement Lab Support <support@measurementlab.net>

RUN apk add --update build-base gcc cmake libressl-dev curl-dev git linux-headers
RUN git clone https://github.com/measurement-kit/libndt.git
WORKDIR /libndt
#RUN git checkout 41e93c6a64684603e76ef686197877c749ae9c98

RUN cmake .
RUN cmake --build . -j $(nproc)
RUN ctest -a --output-on-failure .

# Murakami image
FROM python:3-alpine3.10
RUN apk add git curl libstdc++ libgcc
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

CMD python -m murakami
