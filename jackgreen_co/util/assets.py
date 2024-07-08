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

import os
from typing import Self

from flask import Flask, current_app
from flask import url_for as flask_url_for


class Assets(object):
    def __init__(self: Self):
        pass

    def init_app(self: Self, app: Flask):
        manifest_path = os.path.join(app.static_folder, app.config["ASSETS_MANIFEST"])

        with app.app_context(), open(manifest_path, "r") as f:
            manifest = {}
            for line in f:
                original, hashed = line.strip().split(":")
                manifest[original] = hashed
            app.manifest = manifest


def url_for(endpoint: str, filename: str = None, **values: dict) -> str:
    if endpoint == "static":
        manifest = current_app.manifest
        if filename in manifest:
            filename = manifest[filename]
    return flask_url_for(endpoint, filename=filename, **values)


assets = Assets()
