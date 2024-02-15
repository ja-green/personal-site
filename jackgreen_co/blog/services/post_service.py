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

from flask import current_app

from jackgreen_co import core
from jackgreen_co.blog.models import post


def get(terms={}, page=1):
    posts_per_page = current_app.config.get("BLOG_POSTS_PER_PAGE", 10)
    total_posts = core.db.posts.count_documents(terms)
    total_pages = max((total_posts + posts_per_page - 1) // posts_per_page, 1)
    skip = (page - 1) * posts_per_page

    pipeline = [
        {"$match": terms},
        {"$sort": {"date": -1}},
        {"$skip": skip},
        {"$limit": posts_per_page},
        {"$lookup": {"from": "categories", "localField": "categories", "foreignField": "_id", "as": "categories"}},
        {"$lookup": {"from": "tags", "localField": "tags", "foreignField": "_id", "as": "tags"}},
        {
            "$addFields": {
                "categories": {"$map": {"input": "$categories", "as": "category", "in": {"title": "$$category.title"}}},
                "tags": {"$map": {"input": "$tags", "as": "tag", "in": {"title": "$$tag.title"}}},
            }
        },
    ]

    post_documents = list(core.db.posts.aggregate(pipeline))
    posts = [post.Post(post_data) for post_data in post_documents]

    return posts, total_pages
