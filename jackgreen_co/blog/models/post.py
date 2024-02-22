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


class Post:
    def __init__(self, data):
        self.object_id = data.get("_id")
        self.title = data.get("title")
        self.date = data.get("date")
        self.image = data.get("image")
        self.content = data.get("content")
        self.toc = data.get("toc")
        self.preview = data.get("preview")
        self.read_time = data.get("read_time")
        self.slug = data.get("slug")
        self.categories = [Category(c) for c in data.get("categories", [])]
        self.tags = [Tag(t) for t in data.get("tags", [])]

    def __repr__(self):
        return f"<Post {self.title}>"


class Category:
    def __init__(self, data):
        self.object_id = data.get("_id")
        self.title = data.get("title")

    def __repr__(self):
        return f"<Category {self.title}>"


class Tag:
    def __init__(self, data):
        self.object_id = data.get("_id")
        self.title = data.get("title")

    def __repr__(self):
        return f"<Tag {self.title}>"
