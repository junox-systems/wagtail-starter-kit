#!/bin/sh
set -eu

. /usr/local/etc/wagtail/env

exec /usr/local/bin/litestream replicate \
    -config /usr/local/etc/litestream.yml
