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

from flask import render_template
from flask.typing import ResponseReturnValue

from jackgreen_co.main import main
from jackgreen_co.main.messages import Messages


@main.errorhandler(400)
def e400(_) -> ResponseReturnValue:
    return render_template("main/errors/400.jinja.html", title="Error 400", is_error=True, messages=Messages), 400


@main.errorhandler(404)
def e404(_) -> ResponseReturnValue:
    return render_template("main/errors/404.jinja.html", title="Error 404", is_error=True, messages=Messages), 404


@main.errorhandler(405)
def e405(_) -> ResponseReturnValue:
    return render_template("main/errors/405.jinja.html", title="Error 405", is_error=True, messages=Messages), 405


@main.errorhandler(500)
def e500(_) -> ResponseReturnValue:
    return render_template("main/errors/500.jinja.html", title="Error 500", is_error=True, messages=Messages), 500
