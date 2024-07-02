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

from flask import current_app, render_template, request
from flask.typing import ResponseReturnValue


def route_error(e: int) -> ResponseReturnValue:
    subdomain = request.host[: -len(current_app.config["SERVER_NAME"])].rstrip(".") or None
    path = request.path or ""

    for bp_name, bp in current_app.blueprints.items():
        if subdomain == bp.subdomain and path.startswith(bp.url_prefix or ""):
            handler = current_app.error_handler_spec.get(bp_name, {}).get(e)

            if handler is not None:
                handler = list(handler.values())[0]
                return handler(e)

    return render_template("errors/%s.jinja.html" % (e), title="Error %s" % (e), is_error=True), e


def global_e400(_) -> ResponseReturnValue:
    return route_error(400)


def global_e404(_) -> ResponseReturnValue:
    return route_error(404)


def global_e405(_) -> ResponseReturnValue:
    return route_error(405)


def global_e500(_) -> ResponseReturnValue:
    return route_error(500)
