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

import secrets
from datetime import timedelta
from typing import Self

import msgpack
from flask import Flask, Request, Response
from flask.sessions import SessionInterface, SessionMixin
from redis.client import StrictRedis
from werkzeug.datastructures import CallbackDict


class RedisSession(CallbackDict, SessionMixin):
    def __init__(self: Self, initial: dict = None, sid: str = None):
        def on_update(self: Self):
            self.modified = True

        super(RedisSession, self).__init__(initial, on_update)
        self.sid = sid
        self.modified = False


class RedisSessionInterface(SessionInterface):
    serializer = msgpack
    session_class = RedisSession

    def __init__(self: Self, redis: StrictRedis, prefix: str = "session:"):
        self.redis = redis
        self.prefix = prefix
        self.sid_length = 64

    def generate_sid(self: Self) -> str:
        return secrets.token_hex(self.sid_length)

    def get_redis_expiration_time(self: Self, app: Flask, session: RedisSession) -> timedelta:
        if session.permanent:
            return app.permanent_session_lifetime
        return app.config.get("SESSION_LIFETIME", timedelta(minutes=10))

    def open_session(self: Self, app: Flask, request: Request) -> RedisSession:
        sid = request.cookies.get(app.config["SESSION_COOKIE_NAME"])
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid)

        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val, raw=False)
            return self.session_class(data, sid=sid)

        return self.session_class(sid=sid)

    def save_session(self: Self, app: Flask, session: RedisSession, response: Response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(
                    app.config["SESSION_COOKIE_NAME"],
                    domain=domain,
                    path=path,
                )
            return

        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)

        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, int(redis_exp.total_seconds()), val)
        response.set_cookie(
            app.config["SESSION_COOKIE_NAME"],
            session.sid,
            expires=cookie_exp,
            httponly=True,
            domain=domain,
            path=path,
            secure=(app.config["ENV"] != "development"),
        )
