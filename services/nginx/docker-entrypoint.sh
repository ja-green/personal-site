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

ln -sf /dev/stdout /var/log/nginx/stdout-access.log
ln -sf /dev/stdout /var/log/nginx/stdout-error.log

touch /var/log/nginx/access.log
touch /var/log/nginx/error.log

control_pipe="/etc/nginx/control/pipe"

if [ -e "${control_pipe}" ]; then
    rm -f "${control_pipe}"
fi

mkfifo "${control_pipe}"

send_nginx_signal() {
    signal=${1}
    nginx_pid=$(cat /var/run/nginx.pid)

    if [ -n "${nginx_pid}" ]; then
        kill -${signal} ${nginx_pid}
        echo "Signal ${signal} sent to nginx"
    fi
}

(
    echo "Started nginx signal listener"
    while true; do
        if read line < "${control_pipe}"; then
            echo "Received command: ${line}"
            case "${line}" in
                reopen_logs)
                    send_nginx_signal USR1
                    ;;
                reload)
                    send_nginx_signal HUP
                    ;;
                *)
                    echo "Unknown command: ${line}"
                    ;;
            esac
        fi
    done
) &

exec "${@}"
