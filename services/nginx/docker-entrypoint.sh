#!/usr/bin/env sh

# Copyright (C) 2024 Jack Green (jackgreen.co)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

set -e

if [ "${BUILD_ENV}" = "staging" ]; then
    sed -i 's/ssl_stapling on;/ssl_stapling off;/g' /etc/nginx/nginx.conf
    sed -i 's/ssl_stapling_verify on;/ssl_stapling_verify off;/g' /etc/nginx/nginx.conf
fi

exec "${@}"
