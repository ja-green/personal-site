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

from typing import Self

import redis as redis_py
from flask import Flask
from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient
from redis.exceptions import ConnectionError


class MongoWrapper(object):
    def __init__(self: Self):
        self.db = None

    def init_app(self: Self, app: Flask):
        mongo_config = {
            key[len("MONGO_") :].lower(): value for key, value in app.config.items() if key.startswith("MONGO_")
        }
        mongo_dbname = mongo_config.pop("dbname", None)

        try:
            self.client = MongoClient(**mongo_config)
            self.db = self.client[mongo_dbname]
            self.client.admin.command("ismaster")

        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}", flush=True)
            self.db = None
        except Exception as e:
            print(f"An error occurred while initializing MongoDB: {e}", flush=True)
            self.db = None


class RedisWrapper(object):
    def __init__(self: Self):
        self.redis = None

    def init_app(self: Self, app: Flask):
        redis_config = {
            key[len("REDIS_") :].lower(): value for key, value in app.config.items() if key.startswith("REDIS_")
        }

        redis_ssl = redis_config.pop("ssl", False)

        try:
            if redis_ssl:
                redis_config["connection_class"] = redis_py.SSLConnection
            else:
                redis_config["connection_class"] = redis_py.Connection

            pool = redis_py.ConnectionPool(**redis_config)
            self.redis = redis_py.StrictRedis(connection_pool=pool, ssl=redis_ssl)
            self.redis.ping()

        except ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            self.redis = None
        except Exception as e:
            print(f"An error occurred while initializing Redis: {e}")
            self.redis = None


db_client = MongoWrapper()
db = None
redis_client = RedisWrapper()
redis = None
