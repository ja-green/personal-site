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

from flask import Flask

from config import config
from jackgreen_co import core
from jackgreen_co.blog import blog as bp_blog
from jackgreen_co.core import context, errors, hook, routes, session
from jackgreen_co.main import main as bp_main
from jackgreen_co.util import assets, features, mail, minify


def init() -> Flask:
    app = Flask(
        __name__,
        static_url_path="/assets",
        static_folder="core/static",
        template_folder="core/templates",
        subdomain_matching=True,
    )

    config.init_app(app)
    core.db_client.init_app(app)
    core.db = core.db_client.db
    core.redis_client.init_app(app)
    core.redis = core.redis_client.redis
    features.features.init_app(app)
    assets.assets.init_app(app)
    mail.mail.init_app(app)
    minify.minify.init_app(app, core.redis)

    app.session_interface = session.RedisSessionInterface(core.redis)

    app.jinja_env.globals["url_for"] = assets.url_for
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.add_extension("jinja2.ext.do")

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_blog)

    if app.config["ENV"] == "development":
        app.after_request(hook.after_request)

    app.add_url_rule("/sitemap.xml", "core.sitemap", routes.sitemap)
    app.add_url_rule("/sitemap", "core.sitemap", routes.sitemap)
    app.add_url_rule("/manifest.webmanifest", "core.webmanifest", routes.webmanifest)
    app.add_url_rule("/manifest.json", "core.webmanifest", routes.webmanifest)

    app.register_error_handler(400, errors.global_e400)
    app.register_error_handler(404, errors.global_e404)
    app.register_error_handler(405, errors.global_e405)
    app.register_error_handler(500, errors.global_e500)

    app.context_processor(context.current_date)
    app.context_processor(context.messages)
    app.context_processor(context.endpoint)
    app.context_processor(context.features)
    app.context_processor(context.theme)

    return app
