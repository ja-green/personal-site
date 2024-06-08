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

from flask import render_template
from flask.typing import ResponseReturnValue

from jackgreen_co.blog import blog
from jackgreen_co.blog.messages import Messages


@blog.errorhandler(400)
def e400() -> ResponseReturnValue:
    return render_template("blog/errors/400.jinja.html", title="Error 400", is_error=True, messages=Messages), 400


@blog.errorhandler(404)
def e404() -> ResponseReturnValue:
    return render_template("blog/errors/404.jinja.html", title="Error 404", is_error=True, messages=Messages), 404


@blog.errorhandler(405)
def e405() -> ResponseReturnValue:
    return render_template("blog/errors/405.jinja.html", title="Error 405", is_error=True, messages=Messages), 405


@blog.errorhandler(500)
def e500() -> ResponseReturnValue:
    return render_template("blog/errors/500.jinja.html", title="Error 500", is_error=True, messages=Messages), 500
