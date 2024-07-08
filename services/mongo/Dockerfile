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

FROM mongo:latest

RUN mkdir -p /etc/ssl /var/log/mongo

COPY ./build/initdb.js /docker-entrypoint-initdb.d/initdb.js
COPY ./services/mongo/mongod.conf /etc/mongo/mongod.conf
COPY ./build/ssl/mongo.pem /etc/ssl/internal/mongo.pem
COPY ./build/ssl/ca.pem /etc/ssl/internal/ca.pem

RUN rm -rf /data/db
RUN chown -R mongodb:mongodb /etc/ssl /var/log/mongo /etc/mongo /docker-entrypoint-initdb.d

EXPOSE 27017

CMD ["mongod", "--quiet", "--config", "/etc/mongo/mongod.conf"]
