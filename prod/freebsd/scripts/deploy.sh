#!/bin/sh
set -eu

APP_USER="www"
APP_DIR="/usr/local/www/wagtail"
LOCK="/tmp/wagtail-deploy.lock"
VENV_PY=".venv/bin/python"

cd "$APP_DIR"

echo "==== $(date '+%Y-%m-%d %H:%M:%S') ===="

# ---- lock ----
if [ -f "$LOCK" ]; then
    echo "== deploy already running =="
    exit 0
fi

trap 'rm -f "$LOCK"' EXIT
touch "$LOCK"

echo "== deploy start =="

# ---- helper ----
run_app() {
    su -m "$APP_USER" -c "cd $APP_DIR && sh -c '$1'"
}

# ---- check for updates ----
run_app "git fetch origin"

LOCAL=$(run_app "git rev-parse HEAD" | tr -d '\n')
REMOTE=$(run_app "git rev-parse origin/main" | tr -d '\n')

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "== no changes =="
    exit 0
fi

echo "== updating =="
run_app "git pull --ff-only"

# ---- app updates ----
echo "== setting up pip requirements =="
just setup-pip

echo "== collecting static files =="
run_app "$VENV_PY manage.py collectstatic --no-input --clear"

echo "== migrating =="
run_app "DJANGO_SETTINGS_MODULE=config.settings.prod $VENV_PY manage.py migrate"

# ---- restart ----
echo "== restarting =="
just prod-start

echo "== deploy done =="
