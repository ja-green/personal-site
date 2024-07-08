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

REDIS_CONFIG="/etc/redis/redis.conf"

if [ -n "${REDIS_INITDB_USERNAME}" ] && [ -n "${REDIS_INITDB_PASSWORD}" ]; then
    echo "Setting up Redis ACL for user ${REDIS_INITDB_USERNAME}..."
    printf "user ${REDIS_INITDB_USERNAME} on >${REDIS_INITDB_PASSWORD} +@all &* ~*\nuser default off\n" > /etc/redis/users.acl
elif [ -n "${REDIS_INITDB_PASSWORD}" ]; then
    echo "Setting up Redis password..."
    printf "user default on >${REDIS_INITDB_PASSWORD} +@all -@dangerous &* ~*\n" > /etc/redis/users.acl
else
    echo "Setting up Redis ACL for default user..."
    printf "user default on nopass +@all -@dangerous &* ~*\n" > /etc/redis/users.acl
fi

if [ "${1#-}" != "${1}" ] || [ "${1%.conf}" != "${1}" ]; then
    set -- redis-server "${@}" ${REDIS_CONFIG}
fi

if [ "${1}" = 'redis-server' -a "$(id -u)" = '0' ]; then
    chown -R redis /etc/redis
    exec gosu redis "${0}" "${@}"
fi

exec "$@"
