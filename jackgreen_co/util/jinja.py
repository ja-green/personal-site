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

from typing import Self
from urllib.parse import urlparse

from flask import Flask


class Jinja(object):
    def __init__(self: Self):
        pass

    def init_app(self: Self, app: Flask):
        self.server_name = app.config["SERVER_NAME"]

    def is_external_url(self: Self, url: str) -> bool:
        parsed_url = urlparse(url)

        if parsed_url.netloc:
            return parsed_url.netloc != self.server_name
        return False


jinja = Jinja()
