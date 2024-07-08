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

from flask import current_app

from jackgreen_co import core
from jackgreen_co.blog.models import post


def get(terms: dict = {}, limit: int = None, page: int = None) -> tuple[list[post.Category], int]:
    categories_per_page = current_app.config.get("BLOG_CATEGORIES_PER_PAGE", 10)
    total_categories = core.db.categories.count_documents(terms)

    if limit is not None:
        categories_to_fetch = min(limit, total_categories)
        total_pages = 1
        skip = 0
    elif page is not None:
        total_pages = max((total_categories + categories_per_page - 1) // categories_per_page, 1)
        skip = (page - 1) * categories_per_page
        categories_to_fetch = categories_per_page
    else:
        total_pages = max((total_categories + categories_per_page - 1) // categories_per_page, 1)
        skip = 0
        categories_to_fetch = total_categories

    pipeline = [
        {"$match": terms},
        {"$sort": {"title": 1}},
    ]

    if skip > 0:
        pipeline.append({"$skip": skip})
    if limit is not None or page is not None:
        pipeline.append({"$limit": categories_to_fetch})

    category_documents = list(core.db.categories.aggregate(pipeline))
    categories = [post.Category(category_data) for category_data in category_documents]

    return categories, total_pages
