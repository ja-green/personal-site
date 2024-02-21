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
from datetime import timedelta


class Config(object):
    def load(self, env=os.environ.get("FLASK_ENV")):
        if env == "production":
            return ConfigProd
        return ConfigDev

    def parse(self, env=os.environ.get("FLASK_ENV"), obj=None):
        config = {}
        if not obj:
            obj = self.load(env)

        for key in dir(obj):
            if key.isupper():
                config[key] = getattr(obj, key)

        return config

    def init_app(self, app):
        c = self.parse()
        app.config.from_mapping(c)


class BaseConfig(object):
    SECRET_KEY = secrets.token_hex(64)
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    SITE_NAME = "Jack Green"
    SITE_AUTHOR = "Jack Green"
    ASSETS_MANIFEST = "manifest.txt"
    SESSION_LIFETIME = timedelta(minutes=10)
    BLOG_POSTS_PER_PAGE = 2


class ConfigDev(BaseConfig):
    ENV = "development"
    DEBUG = True
    SERVER_NAME = "jackgreen.co:8000"
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_DBNAME = "jackgreen_co"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379


class ConfigProd(BaseConfig):
    ENV = "production"
    DEBUG = False
    SERVER_NAME = "jackgreen.co"


config = Config()
