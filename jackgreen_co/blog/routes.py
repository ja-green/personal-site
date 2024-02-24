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

from flask import abort, redirect, render_template, request, url_for

from jackgreen_co.blog import blog
from jackgreen_co.blog.services import category_service, post_service


@blog.route("/")
def index():
    return redirect(url_for("blog.posts", page=1), code=301)


@blog.route("/posts")
def posts():
    page = request.args.get("page", 1, type=int)
    posts, total_pages = post_service.get(page=page)
    categories, _ = category_service.get(limit=5)
    if not posts or len(posts) == 0:
        abort(404)
    return render_template(
        "blog/posts/list.jinja.html", page=page, posts=posts, total_pages=total_pages, categories=categories
    )


@blog.route("/posts/<slug>")
def post(slug):
    posts, _ = post_service.get({"slug": slug})
    if not posts:
        abort(404)
    if len(posts) > 1:
        abort(500)

    return render_template("blog/posts/single.jinja.html", post=posts[0])


@blog.route("/categories")
def categories():
    page = request.args.get("page", 1, type=int)
    categories, total_pages = category_service.get(page=page)
    all_categories, _ = category_service.get()
    posts = {
        category.object_id: post_service.get({"categories": category.object_id}, limit=3)[0] for category in categories
    }
    if not categories or len(categories) == 0:
        abort(404)
    return render_template(
        "blog/categories/list.jinja.html",
        page=page,
        categories=categories,
        total_pages=total_pages,
        posts=posts,
        all_categories=all_categories,
    )
