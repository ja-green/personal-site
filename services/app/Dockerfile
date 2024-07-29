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

RUN mkdir -p /app /data /etc/gunicorn /etc/ssl

RUN apk add --no-cache python3 py3-pip rust cargo && \
    pip3 install --no-cache --break-system-packages --upgrade pip setuptools

COPY ./requirements.txt /app
RUN pip3 install --no-cache --break-system-packages -r /app/requirements.txt && \
    pip3 install --no-cache --break-system-packages gunicorn

COPY ./jackgreen_co/ /app/jackgreen_co/
COPY ./config.py /app
COPY ./wsgi.py /app

COPY ./services/app/gunicorn.py /etc/gunicorn/gunicorn.py
COPY ./build/ssl/mongo-cert.pem /etc/ssl/internal/mongo-cert.pem
COPY ./build/ssl/redis-cert.pem /etc/ssl/internal/redis-cert.pem
COPY ./build/ssl/app-cert.pem /etc/ssl/internal/app-cert.pem
COPY ./build/ssl/app-key.pem /etc/ssl/internal/app-key.pem
COPY ./build/ssl/app.pem /etc/ssl/internal/app.pem
COPY ./build/ssl/ca.pem /etc/ssl/internal/ca.pem

RUN addgroup -S www && adduser -S -G www www && \
    chown -R www:www /app /data /etc/gunicorn /etc/ssl

EXPOSE 8000

CMD ["gunicorn", "--config", "/etc/gunicorn/gunicorn.py", "--chdir", "/app", "wsgi:app"]
