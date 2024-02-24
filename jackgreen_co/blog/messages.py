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

from jackgreen_co.core import messages


class Messages(messages.Messages):
    blog_posts_description = "TODO: Add a description here."
    blog_posts_heading = "Posts"
    blog_posts_subheading = "Explore and read my blog posts."
    blog_posts_viewcategories = "View all categories"

    blog_post_toc_heading = "Contents"
    blog_post_categories_heading = "Categories"
    blog_post_tags_heading = "Tags"

    blog_categories_description = "TODO: Add a description here."
    blog_categories_heading = "Categories"
    blog_categories_subheading = "Explore my blog posts by category."
    blog_categories_seeall = "See all posts in %s"
    blog_categories_showing_singular = "Showing %s of %s post"
    blog_categories_showing_plural = "Showing %s of %s posts"
    blog_categories_all_heading = "All Categories"

    blog_error_action = "Go back to posts"
