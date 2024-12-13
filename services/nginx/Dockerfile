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

RUN apk update && apk add --no-cache openresty openssl

RUN deluser nginx; addgroup -g 1000 -S nginx && adduser -u 1000 -S nginx -G nginx

RUN mkdir -p /etc/ssl /var/log/nginx /var/lib/nginx
RUN rm -rf /usr/share/nginx/html/* /var/log/nginx/*

COPY ./services/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./services/nginx/error-pages /usr/share/nginx/html/error-pages
COPY ./build/ssl/nginx-cert.pem /etc/ssl/internal/nginx-cert.pem
COPY ./build/ssl/nginx-key.pem /etc/ssl/internal/nginx-key.pem
COPY ./build/ssl/ca.pem /etc/ssl/internal/ca.pem
COPY ./jackgreen_co/core/static /usr/share/nginx/html/assets

RUN chown -R nginx:nginx /usr/share/nginx/html /etc/ssl /var/log/nginx /var/lib/nginx

COPY ./services/nginx/docker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +rx /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]
