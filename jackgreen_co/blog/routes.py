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

from flask import abort, make_response, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue

from jackgreen_co.blog import blog
from jackgreen_co.blog.services import category_service, post_service, tag_service, series_service


@blog.route("/")
def index() -> ResponseReturnValue:
    return redirect(url_for("blog.posts", page=1), code=301)


@blog.route("/posts")
def posts() -> ResponseReturnValue:
    page = request.args.get("page", 1, type=int)
    if page < 1:
        return redirect(url_for("blog.posts", page=1), code=301)
    posts, total_pages = post_service.get(page=page)
    if not posts or len(posts) == 0:
        abort(404)

    series, _ = series_service.get(limit=5)
    categories, _ = category_service.get(limit=5)
    tags, _ = tag_service.get(limit=10)

    return render_template(
        "blog/posts/list.jinja.html",
        page=page,
        posts=posts,
        total_pages=total_pages,
        categories=categories,
        tags=tags,
        series=series,
    )


@blog.route("/posts/<slug>")
def post(slug: str) -> ResponseReturnValue:
    posts, _ = post_service.get({"slug": slug})
    if not posts:
        abort(404)
    if len(posts) > 1:
        abort(500)

    prev_post = None
    next_post = None

    post = posts[0]

    if post.series:
        prev_post, _ = post_service.get({"series_index": post.series_index - 1, "series": post.series.object_id})
        next_post, _ = post_service.get({"series_index": post.series_index + 1, "series": post.series.object_id})

    prev_post = None if not prev_post or len(prev_post) == 0 else prev_post[0]
    next_post = None if not next_post or len(next_post) == 0 else next_post[0]

    return render_template(
        "blog/posts/single.jinja.html", title=post.title, post=post, prev_post=prev_post, next_post=next_post
    )


@blog.route("/series")
def series() -> ResponseReturnValue:
    page = request.args.get("page", 1, type=int)
    if page < 1:
        return redirect(url_for("blog.series", page=1), code=301)
    series, total_pages = series_service.get(page=page)
    if not series or len(series) == 0:
        abort(404)
    all_series, _ = series_service.get()
    posts = {series.object_id: post_service.get({"series": series.object_id}, limit=3)[0] for series in series}
    return render_template(
        "blog/series/list.jinja.html",
        page=page,
        series=series,
        total_pages=total_pages,
        posts=posts,
        all_series=all_series,
    )


@blog.route("/series/<slug>")
def singleseries(slug: str) -> ResponseReturnValue:
    page = request.args.get("page", 1, type=int)
    if page < 1:
        return redirect(url_for("blog.single_series", slug=slug, page=1), code=301)
    series, _ = series_service.get({"slug": slug})
    if not series:
        abort(404)
    if len(series) > 1:
        abort(500)
    series_item = series[0]
    posts, total_pages = post_service.get({"series": series_item.object_id}, page=page)
    if not posts or len(posts) == 0:
        abort(404)
    series, _ = series_service.get(limit=5)
    categories, _ = category_service.get(limit=5)
    tags, _ = tag_service.get(limit=10)
    return render_template(
        "blog/series/single.jinja.html",
        title=series_item.title,
        series_item=series_item,
        page=page,
        posts=posts,
        total_pages=total_pages,
        series=series,
        categories=categories,
        tags=tags,
    )


@blog.route("/categories")
def categories() -> ResponseReturnValue:
    page = request.args.get("page", 1, type=int)
    if page < 1:
        return redirect(url_for("blog.categories", page=1), code=301)
    categories, total_pages = category_service.get(page=page)
    if not categories or len(categories) == 0:
        abort(404)
    all_categories, _ = category_service.get()
    posts = {
        category.object_id: post_service.get({"categories": category.object_id}, limit=3)[0] for category in categories
    }
    return render_template(
        "blog/categories/list.jinja.html",
        page=page,
        categories=categories,
        total_pages=total_pages,
        posts=posts,
        all_categories=all_categories,
    )


@blog.route("/categories/<slug>")
def category(slug: str) -> ResponseReturnValue:
    page = request.args.get("page", 1, type=int)
    if page < 1:
        return redirect(url_for("blog.category", slug=slug, page=1), code=301)
    categories, _ = category_service.get({"slug": slug})
    if not categories:
        abort(404)
    if len(categories) > 1:
        abort(500)
    category = categories[0]
    posts, total_pages = post_service.get({"categories": category.object_id}, page=page)
    if not posts or len(posts) == 0:
        abort(404)
    series, _ = series_service.get(limit=5)
    categories, _ = category_service.get(limit=5)
    tags, _ = tag_service.get(limit=10)
    return render_template(
        "blog/categories/single.jinja.html",
        title=category.title,
        category=category,
        page=page,
        posts=posts,
        total_pages=total_pages,
        series=series,
        categories=categories,
        tags=tags,
    )


@blog.route("/tags")
def tags() -> ResponseReturnValue:
    page = request.args.get("page", 1, type=int)
    if page < 1:
        return redirect(url_for("blog.tags", page=1), code=301)
    tags, total_pages = tag_service.get(page=page)
    if not tags or len(tags) == 0:
        abort(404)
    all_tags, _ = tag_service.get()
    posts = {tag.object_id: post_service.get({"tags": tag.object_id}, limit=3)[0] for tag in tags}
    return render_template(
        "blog/tags/list.jinja.html", page=page, tags=tags, total_pages=total_pages, posts=posts, all_tags=all_tags
    )


@blog.route("/tags/<slug>")
def tag(slug: str) -> ResponseReturnValue:
    page = request.args.get("page", 1, type=int)
    if page < 1:
        return redirect(url_for("blog.tag", slug=slug, page=1), code=301)
    tags, _ = tag_service.get({"slug": slug})
    if not tags:
        abort(404)
    if len(tags) > 1:
        abort(500)
    tag = tags[0]
    posts, total_pages = post_service.get({"tags": tag.object_id}, page=page)
    if not posts or len(posts) == 0:
        abort(404)
    series, _ = series_service.get(limit=5)
    categories, _ = category_service.get(limit=5)
    tags, _ = tag_service.get(limit=10)
    return render_template(
        "blog/tags/single.jinja.html",
        title=tag.title.title(),
        tag=tag,
        page=page,
        posts=posts,
        total_pages=total_pages,
        series=series,
        categories=categories,
        tags=tags,
    )


@blog.route("/rss")
def rss() -> ResponseReturnValue:
    posts, _ = post_service.get()

    latest_date = None
    for post in posts:
        if not latest_date or post.date > latest_date:
            latest_date = post.date

    body = render_template("blog/rss.jinja.xml", posts=posts, build_date=latest_date)
    response = make_response(body)
    response.headers["Content-Type"] = "application/rss+xml"

    return response
