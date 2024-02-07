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

from urllib.parse import urlparse

from flask import current_app, make_response, render_template, request


def sitemap():
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
                url = {"loc": "%s://%s%s%s" % (host_components.scheme, subdomain, host_components.netloc, str(rule))}
                static_urls.append(url)

    body = render_template("sitemap.jinja.xml", static_urls=static_urls, dynamic_urls=dynamic_urls)
    response = make_response(body)
    response.headers["Content-Type"] = "application/xml"

    return response


def webmanifest():
    body = render_template("webmanifest.jinja.json")
    response = make_response(body)
    response.headers["Content-Type"] = "application/manifest+json"

    return response
