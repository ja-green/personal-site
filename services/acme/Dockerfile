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

FROM alpine:latest

RUN apk add --no-cache curl socat openssl
RUN curl --silent https://raw.githubusercontent.com/acmesh-official/acme.sh/master/acme.sh | \
    sh -s -- --install-online

COPY ./services/acme/docker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +rx /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

EXPOSE 443
