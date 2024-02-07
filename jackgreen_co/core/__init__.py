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

import redis as redis_py
from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient
from redis.exceptions import ConnectionError


class MongoWrapper(object):
    def __init__(self):
        self.db = None

    def init_app(self, app):
        mongo_config = {
            key[len("MONGO_") :].lower(): value for key, value in app.config.items() if key.startswith("MONGO_")
        }

        del mongo_config["dbname"]

        try:
            self.client = MongoClient(**mongo_config)
            self.db = self.client[app.config["MONGO_DBNAME"]]
            self.client.admin.command("ismaster")
        except ConnectionFailure:
            print("Failed to connect to MongoDB")
            self.db = None
        except Exception as e:
            print(f"An error occurred while initializing MongoDB: {e}")
            self.db = None


class RedisWrapper(object):
    def __init__(self):
        self.redis = None

    def init_app(self, app):
        redis_config = {
            key[len("REDIS_") :].lower(): value for key, value in app.config.items() if key.startswith("REDIS_")
        }

        try:
            self.redis = redis_py.StrictRedis(**redis_config)
            self.redis.ping()
        except ConnectionError:
            print("Failed to connect to Redis")
            self.redis = None
        except Exception as e:
            print(f"An error occurred while initializing Redis: {e}")
            self.redis = None


db_client = MongoWrapper()
db = None
redis_client = RedisWrapper()
redis = None
