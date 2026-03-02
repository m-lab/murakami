# ============================================================
# Stage 1: Builder — install dependencies in an isolated layer
# ============================================================
FROM python:3.14-slim-bookworm AS builder

# Install uv for ultra-fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy only dependency manifests first (layer cache optimization)
COPY pyproject.toml uv.lock ./

# Install dependencies into the system Python (no venv needed in container)
RUN uv sync --frozen --no-dev --no-install-project

# Copy application code
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

# ============================================================
# Stage 2: Go Builder — build test clients
# ============================================================
FROM golang:1.23-bookworm AS go-builder

RUN apt-get update && apt-get install -y git

ENV GO111MODULE=on

RUN go install github.com/neubot/dash/cmd/dash-client@master && \
    go install github.com/m-lab/ndt7-client-go/cmd/ndt7-client && \
    go install github.com/m-lab/ndt5-client-go/cmd/ndt5-client

# ============================================================
# Stage 3: Runtime — minimal image with only what's needed
# ============================================================
FROM python:3.14-slim-bookworm AS runtime

# Install system dependencies
RUN apt-key adv --verbose --keyserver hkp://keyserver.ubuntu.com --recv-keys 'B5A08F01796E7F521861B449372D1FF271F2DD50' && \
    echo "deb http://deb.ooni.org/ unstable main" | tee /etc/apt/sources.list.d/ooniprobe.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        git gcc libc-dev libffi-dev libssl-dev make rustc cargo curl \
        ooniprobe-cli && \
    curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash && \
    apt-get install -y speedtest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Security: run as non-root
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy Go binaries
COPY --from=go-builder /go/bin /app/bin

# Copy application code
COPY --from=builder /app .

# Copy speedtest config
COPY ./configs/speedtest-cli.json /home/appuser/.config/ookla/

# Put the venv on PATH
ENV PATH="/app/.venv/bin:/app/bin:${PATH}"

# Add binaries' path to PATH
ENV PYTHONPATH="/app"

# Drop privileges
USER appuser

ENTRYPOINT ["python", "-m", "murakami"]
