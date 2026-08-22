# Copyright (c) 2025-2026 hakergeniusz
#
# Licensed under the EUPL, Version 1.2 or - as soon they will be approved by the European
# Commission - subsequent versions of the EUPL (the "Licence"); You may not use this work
# except in compliance with the Licence.
#
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the Licence for the specific language

# Buildable with podman or docker.
#
# Build:  podman build -t discord-bot .
# Run:    podman run --rm -e DISCORD_BOT_TOKEN=... -e GEMINI_API_KEY=... discord-bot
#         (optionally mount config: -v ./config.yaml:/app/config.yaml:Z)

FROM docker.io/library/python:3.14-slim

LABEL org.opencontainers.image.title="discord-bot" \
    org.opencontainers.image.description="Yet Another Shitly Made Discord Bot." \
    org.opencontainers.image.licenses="EUPL-1.2"

# FFmpeg is required at runtime for music playback (yt-dlp pipes through it).
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# uv from PyPI rather than the astral-sh image: its wheels cover amd64, arm64
# and riscv64, while the image only ships the first two.
RUN pip install --no-cache-dir "uv==0.12.5"

# Build dependencies for riscv64: cffi/pynacl/cryptography lack riscv64 wheels
# and must compile from source. cryptography needs Rust (maturin has riscv64 wheel,
# rust stable ships riscv64gc-unknown-linux-gnu target).
# These are only needed on riscv64; on amd64/arm64 the wheels satisfy everything.
ARG TARGETPLATFORM
RUN if [ "$TARGETPLATFORM" = "linux/riscv64" ]; then \
        apt-get update && \
        apt-get install -y --no-install-recommends \
            build-essential \
            pkg-config \
            libffi-dev \
            libssl-dev \
            python3-dev && \
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path && \
        . "$HOME/.cargo/env" && \
        rustup target add riscv64gc-unknown-linux-gnu && \
        rm -rf /var/lib/apt/lists/*; \
    fi

ENV UV_PYTHON_PREFERENCE=only-system \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:/root/.cargo/bin:$PATH" \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# Install dependencies first so this layer is cached until the lockfile changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# docs/README.md is needed because hatchling uses it as the package readme.
COPY src ./src
COPY docs/README.md ./docs/README.md
RUN uv sync --frozen --no-dev

# Run as an unprivileged user.
RUN useradd --create-home bot
USER bot

CMD ["bot"]
