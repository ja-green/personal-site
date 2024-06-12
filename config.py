# Copyright (C) 2024 Jack Green (jackgreen.co)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import secrets
from datetime import datetime, timedelta
from typing import Self

from flask import Flask


class BaseConfig(object):
    SECRET_KEY = secrets.token_hex(64)
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    SITE_NAME = "Jack Green"
    SITE_AUTHOR = "Jack Green"
    ASSETS_MANIFEST = "manifest.txt"
    SESSION_LIFETIME = timedelta(minutes=10)
    BLOG_POSTS_PER_PAGE = 2
    PRIVACY_LAST_UPDATED = datetime(2024, 6, 12)


class ConfigDev(BaseConfig):
    ENV = "development"
    DEBUG = True
    SERVER_NAME = "localhost:8000"
    MINIFY_USE_CACHE = False
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_TLS = False
    MONGO_DBNAME = "jackgreen_co"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_SSL = False


class ConfigStaging(BaseConfig):
    ENV = "staging"
    DEBUG = True
    SERVER_NAME = "jackgreen.co"
    MINIFY_USE_CACHE = True
    MONGO_HOST = "mongo"
    MONGO_PORT = 27017
    MONGO_DBNAME = "jackgreen_co"
    MONGO_TLS = True
    MONGO_TLSCAFILE = "/etc/ssl/internal/ca.pem"
    MONGO_TLSCERTIFICATEKEYFILE = "/etc/ssl/internal/app.pem"
    MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    REDIS_HOST = "redis"
    REDIS_PORT = 6379
    REDIS_SSL = True
    REDIS_SSL_CA_CERTS = "/etc/ssl/internal/ca.pem"
    REDIS_SSL_CERT_REQS = "required"
    REDIS_SSL_CERTFILE = "/etc/ssl/internal/app-cert.pem"
    REDIS_SSL_KEYFILE = "/etc/ssl/internal/app-key.pem"
    REDIS_USERNAME = os.environ.get("REDIS_USERNAME")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")


class ConfigProd(BaseConfig):
    ENV = "production"
    DEBUG = False
    SERVER_NAME = "jackgreen.co"
    MINIFY_USE_CACHE = True
    MONGO_HOST = "mongo"
    MONGO_PORT = 27017
    MONGO_DBNAME = "jackgreen_co"
    MONGO_TLS = True
    MONGO_TLSCAFILE = "/etc/ssl/internal/ca.pem"
    MONGO_TLSCERTIFICATEKEYFILE = "/etc/ssl/internal/app.pem"
    MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    REDIS_HOST = "redis"
    REDIS_PORT = 6379
    REDIS_SSL = True
    REDIS_SSL_CA_CERTS = "/etc/ssl/internal/ca.pem"
    REDIS_SSL_CERT_REQS = "required"
    REDIS_SSL_CERTFILE = "/etc/ssl/internal/app-cert.pem"
    REDIS_SSL_KEYFILE = "/etc/ssl/internal/app-key.pem"
    REDIS_USERNAME = os.environ.get("REDIS_USERNAME")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")


class Config(object):
    def load(self: Self, env: str = os.environ.get("BUILD_ENV")) -> BaseConfig:
        if env == "production":
            return ConfigProd
        if env == "staging":
            return ConfigStaging
        return ConfigDev

    def parse(self: Self, env: str = os.environ.get("BUILD_ENV"), obj: BaseConfig = None) -> dict:
        config = {}
        if not obj:
            obj = self.load(env)

        for key in dir(obj):
            if key.isupper():
                config[key] = getattr(obj, key)

        return config

    def init_app(self: Self, app: Flask):
        c = self.parse()
        app.config.from_mapping(c)


config = Config()
