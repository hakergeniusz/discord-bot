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

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_PYTHON_PREFERENCE=only-system \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

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
