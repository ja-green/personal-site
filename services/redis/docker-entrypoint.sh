#!/usr/bin/env sh

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
