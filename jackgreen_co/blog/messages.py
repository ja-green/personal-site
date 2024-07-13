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

from jackgreen_co.core import messages


class Messages(messages.Messages):
    blog_back_to_posts = "Back to posts"
    blog_back_to_series = "Back to series"
    blog_back_to_categories = "Back to categories"
    blog_back_to_tags = "Back to tags"
    blog_minute_read = "%s minute read"

    blog_rss_heading = "Posts RSS Feed"
    blog_rss_description = "Stay up-to-date with my latest blog posts by subscribing to the RSS feed."

    blog_posts_title = "Blog Posts"
    blog_posts_description = "Welcome to my blog. Explore my posts, covering a variety of topics including technology, security, my personal hobbies, and more. Follow along with detailed, educational content."
    blog_posts_heading = "Posts"
    blog_posts_subheading = "Explore and read my blog posts."
    blog_posts_viewseries = "View all series"
    blog_posts_viewcategories = "View all categories"
    blog_posts_viewtags = "View all tags"
    blog_posts_viewrss = "View posts RSS feed"

    blog_post_isseries = "This post is part of a series:"
    blog_post_toc_heading = "Contents"
    blog_post_series_heading = "Series"
    blog_post_categories_heading = "Categories"
    blog_post_tags_heading = "Tags"

    blog_series_title = "Blog Series"
    blog_series_description = "Discover my blog series' covering a variety of topics including technology, security, my personal hobbies, and more. Follow along with detailed, educational content."
    blog_series_heading = "Series"
    blog_series_subheading = "Explore my blog posts by series."
    blog_series_seeall = 'See all posts in "%s"'
    blog_series_showing_singular = "Showing %s of %s post"
    blog_series_showing_plural = "Showing %s of %s posts"
    blog_series_all_heading = "All Series"

    blog_singleseries_description = "Explore the %s series on my blog - %s"
    blog_singleseries_subheading = "Explore posts in %s"

    blog_categories_title = "Blog Categories"
    blog_categories_description = "Discover my blog categories covering a variety of topics including technology, security, my personal hobbies, and more. Follow along with detailed, educational content."
    blog_categories_heading = "Categories"
    blog_categories_subheading = "Explore my blog posts by category."
    blog_categories_seeall = "See all posts in %s"
    blog_categories_showing_singular = "Showing %s of %s post"
    blog_categories_showing_plural = "Showing %s of %s posts"
    blog_categories_all_heading = "All Categories"

    blog_category_description = "Explore the %s category on my blog."
    blog_category_subheading = "Explore posts in %s"

    blog_tags_title = "Blog Tags"
    blog_tags_description = "Discover my blog tags covering a variety of topics including technology, security, my personal hobbies, and more. Follow along with detailed, educational content."
    blog_tags_heading = "Tags"
    blog_tags_subheading = "Explore my blog posts by tag."
    blog_tags_seeall = 'See all posts tagged "%s"'
    blog_tags_showing_singular = "Showing %s of %s post"
    blog_tags_showing_plural = "Showing %s of %s posts"
    blog_tags_all_heading = "All Tags"

    blog_tag_description = 'Explore my blog posts tagged with "%s".'
    blog_tag_subheading = 'Explore posts tagged "%s"'

    blog_error_action = "Go back to posts"
