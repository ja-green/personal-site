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

from datetime import datetime

from flask import current_app, request

from jackgreen_co.core.messages import Messages


def current_date() -> dict:
    return dict(current_date=datetime.utcnow())


def messages() -> dict:
    return dict(messages=Messages)


def endpoint() -> dict:
    return dict(endpoint=request.endpoint)


def features() -> dict:
    return dict(features=current_app.features)


def theme() -> dict:
    theme = request.cookies.get("theme", "dark")
    return dict(theme="light" if theme == "light" else "dark")
