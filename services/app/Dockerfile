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

FROM python:latest

RUN mkdir -p /app /data /etc/gunicorn /etc/ssl

WORKDIR /app

COPY ./jackgreen_co/ /app/jackgreen_co/
COPY ./config.py /app
COPY ./requirements.txt /app
COPY ./wsgi.py /app

COPY ./services/app/gunicorn.py /etc/gunicorn/gunicorn.py
COPY ./build/ssl/mongo-cert.pem /etc/ssl/internal/mongo-cert.pem
COPY ./build/ssl/redis-cert.pem /etc/ssl/internal/redis-cert.pem
COPY ./build/ssl/app-cert.pem /etc/ssl/internal/app-cert.pem
COPY ./build/ssl/app-key.pem /etc/ssl/internal/app-key.pem
COPY ./build/ssl/app.pem /etc/ssl/internal/app.pem
COPY ./build/ssl/ca.pem /etc/ssl/internal/ca.pem

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

RUN groupadd -r www && useradd -r -g www www && \
    chown -R www:www /app /data /etc/gunicorn /etc/ssl

EXPOSE 8000

CMD ["gunicorn", "--config", "/etc/gunicorn/gunicorn.py", "wsgi:app"]
