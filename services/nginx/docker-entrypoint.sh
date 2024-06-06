#!/usr/bin/env sh

set -e

if [ "${BUILD_ENV}" = "staging" ]; then
    sed -i 's/ssl_stapling on;/ssl_stapling off;/g' /etc/nginx/nginx.conf
    sed -i 's/ssl_stapling_verify on;/ssl_stapling_verify off;/g' /etc/nginx/nginx.conf
fi

exec "${@}"
