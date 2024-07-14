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

from urllib.parse import urlparse

from flask import current_app, make_response, render_template, request, url_for
from flask.typing import ResponseReturnValue

from jackgreen_co.blog.services import category_service, post_service, series_service, tag_service


def sitemap() -> ResponseReturnValue:
    host_components = urlparse(request.host_url)

    static_urls = list()
    dynamic_urls = list()

    for bp_name, bp in current_app.blueprints.items():
        for rule in current_app.url_map.iter_rules():
            if (
                "download" not in str(rule)
                and rule.endpoint.split(".")[0] == bp_name
                and "GET" in rule.methods
                and len(rule.arguments) == 0
            ):
                subdomain = bp.subdomain + "." if bp.subdomain else ""
                url = {
                    "loc": "%s://%s%s%s"
                    % (
                        host_components.scheme,
                        subdomain,
                        host_components.netloc,
                        str(rule),
                    )
                }
                static_urls.append(url)

    posts, _ = post_service.get()
    for post in posts:
        url = {
            "loc": "%s" % (url_for("blog.post", slug=post.slug)),
            "lastmod": post.date.strftime("%Y-%m-%d"),
        }
        dynamic_urls.append(url)

    series, _ = series_service.get()
    for series_item in series:
        url = {"loc": "%s" % (url_for("blog.singleseries", slug=series_item.slug))}
        dynamic_urls.append(url)

    categories, _ = category_service.get()
    for category in categories:
        url = {"loc": "%s" % (url_for("blog.category", slug=category.slug))}
        dynamic_urls.append(url)

    tags, _ = tag_service.get()
    for tag in tags:
        url = {"loc": "%s" % (url_for("blog.tag", slug=tag.slug))}
        dynamic_urls.append(url)

    body = render_template("sitemap.jinja.xml", static_urls=static_urls, dynamic_urls=dynamic_urls)
    response = make_response(body)
    response.headers["Content-Type"] = "application/xml"

    return response


def webmanifest() -> ResponseReturnValue:
    origin = request.headers.get("Origin")
    start_url = request.host_url
    if origin:
        start_url = f"{origin}/"
    body = render_template(
        "webmanifest.jinja.json",
        start_url=start_url,
    )
    response = make_response(body)
    response.headers["Content-Type"] = "application/manifest+json"

    origin = request.environ.get("HTTP_ORIGIN")
    if origin and origin.endswith("." + current_app.config["SERVER_NAME"]):
        response.headers["Access-Control-Allow-Origin"] = origin

    return response
