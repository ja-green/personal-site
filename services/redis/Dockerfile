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

FROM redis:latest

RUN mkdir -p /etc/ssl /etc/redis

COPY ./services/redis/redis.conf /etc/redis/redis.conf
COPY ./build/ssl/redis-cert.pem /etc/ssl/internal/redis-cert.pem
COPY ./build/ssl/redis-key.pem /etc/ssl/internal/redis-key.pem
COPY ./build/ssl/ca.pem /etc/ssl/internal/ca.pem

COPY ./services/redis/docker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +rx /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

RUN chown -R redis:redis /etc/ssl /etc/redis

EXPOSE 6379

CMD ["redis-server", "/etc/redis/redis.conf"]
