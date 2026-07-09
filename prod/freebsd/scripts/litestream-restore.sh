#!/bin/sh
set -eu

. /usr/local/etc/wagtail/env

echo "Restoring to $DATABASE_PATH"

exec litestream restore \
  -config /usr/local/etc/litestream.yml \
  -if-replica-exists \
  -o "$DATABASE_PATH" \
  "$DATABASE_PATH"
