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

from flask import redirect, render_template, request, url_for

from jackgreen_co.blog import blog


@blog.route("/")
def index():
    return redirect(url_for("blog.posts", page=1), code=301)


@blog.route("/posts")
def posts():
    page = request.args.get("page", 1, type=int)
    return render_template("blog/posts/list.jinja.html", page=page)
