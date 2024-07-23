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

touch /var/log/nginx/salt
chmod 600 /var/log/nginx/salt
salt="$(openssl rand -hex 32)"
echo "${salt}" > /var/log/nginx/salt

anonymize_logs() {
    salt="${1}"
    log_file="/var/log/nginx/access.log"

    if [ -f "${log_file}" ]; then
        awk -v salt="${salt}" '{
            if ($1 ~ /[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/) {
                cmd = "echo -n "salt$1" | openssl dgst -sha256 | awk \"{print \\$2}\""
                cmd | getline hash
                close(cmd)
                $1 = hash
            }
            print $0
        }' "${log_file}" > "${log_file}.tmp"
        mv "${log_file}.tmp" "${log_file}"
    fi
}

while true; do
    sleep 86400

    echo "Rotating logs"
    anonymize_logs "${salt}"

    salt="$(openssl rand -hex 32)"
    echo "${salt}" > /var/log/nginx/salt

    logrotate -s /var/log/nginx/logrotate.status /etc/logrotate.conf
    echo "reload" > /etc/nginx/control/pipe
done
