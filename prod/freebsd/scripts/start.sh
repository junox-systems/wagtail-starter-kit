#!/bin/sh
set -eu

# ---- CONFIG ---- #

APP_DIR="/usr/local/www/wagtail"
ENV_FILE="/usr/local/etc/wagtail/env"
VENV="/usr/local/www/wagtail/.venv"
SOCK="/var/run/wagtail/wagtail.sock"
export PATH="$VENV/bin:$PATH"

# ---- PREP ---- #

# load environment (must exist)
if [ ! -f "$ENV_FILE" ]; then
    echo "env file missing: $ENV_FILE" >&2
    exit 1
fi

# shellcheck disable=SC1090
. "$ENV_FILE"

# ensure app dir exists
if [ ! -d "$APP_DIR" ]; then
    echo "app dir missing: $APP_DIR" >&2
    exit 1
fi

cd "$APP_DIR"

# ---- SOCKET SAFETY ---- #

# remove stale socket if present
if [ -S "$SOCK" ]; then
    rm -f "$SOCK"
fi

# ---- EXEC ---- #

export DJANGO_SETTINGS_MODULE=config.settings.prod

# ensure mise environment is used from repo
exec "$VENV/bin/python" -m uvicorn config.asgi:application \
    --uds "$SOCK" \
    --workers 1 \
    --loop uvloop \
    --http h11 \
    --limit-concurrency 128 \
    --timeout-keep-alive 128 \
    --backlog 8192 \
    --log-level warning 
