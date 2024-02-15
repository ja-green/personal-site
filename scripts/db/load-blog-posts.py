#!/usr/bin/env python

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

import os
import re
import subprocess
from datetime import datetime

import markdown2
import pymongo
import yaml
from bs4 import BeautifulSoup

PROJECT_ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
AVERAGE_READ_SPEED_WPM = 200
STOP_WORDS = set(
    [
        "a",
        "about",
        "actually",
        "after",
        "against",
        "almost",
        "also",
        "although",
        "always",
        "am",
        "among",
        "an",
        "and",
        "any",
        "are",
        "around",
        "as",
        "at",
        "be",
        "became",
        "become",
        "between",
        "but",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "during",
        "each",
        "either",
        "else",
        "enough",
        "for",
        "from",
        "had",
        "has",
        "have",
        "how",
        "i",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "just",
        "least",
        "let",
        "like",
        "likely",
        "may",
        "nor",
        "not",
        "now",
        "of",
        "on",
        "or",
        "out",
        "over",
        "the",
        "then",
        "through",
        "to",
        "under",
        "when",
        "where",
        "why",
        "with",
        "without",
        "would",
        "yet",
        "you",
        "your",
    ]
)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["jackgreen_co"]
posts_col = db["posts"]
categories_col = db["categories"]
tags_col = db["tags"]


def clean_database():
    posts_col.delete_many({})
    categories_col.delete_many({})
    tags_col.delete_many({})


def find_or_create_category(title):
    category = categories_col.find_one({"title": title})
    if not category:
        result = categories_col.insert_one({"title": title, "post_count": 1})
        category_id = result.inserted_id
    else:
        category_id = category["_id"]
        categories_col.update_one({"_id": category_id}, {"$inc": {"post_count": 1}})
    return category_id


def find_or_create_tag(title):
    tag = tags_col.find_one({"title": title})
    if not tag:
        result = tags_col.insert_one({"title": title, "post_count": 1})
        tag_id = result.inserted_id
    else:
        tag_id = tag["_id"]
        tags_col.update_one({"_id": tag_id}, {"$inc": {"post_count": 1}})
    return tag_id


def generate_slug(title):
    words = title.lower().split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    slug_base = " ".join(filtered_words)

    slug = re.sub(r"[\s_]+", "-", slug_base)
    slug = re.sub(r"[^\w-]", "", slug)
    slug = slug.strip("-")

    return slug


def generate_preview(content, preview_limit=300):
    if len(content) <= preview_limit:
        return content

    end_index = content.rfind(" ", 0, preview_limit)

    if end_index == -1:
        end_index = preview_limit

    preview = content[:end_index] + "..."
    return preview


def calculate_read_time(content):
    word_count = len(re.findall(r"\w+", content))
    read_time = round(word_count / AVERAGE_READ_SPEED_WPM)
    return max(read_time, 1)


def process_categories_and_tags(categories, tags):
    category_ids = [find_or_create_category(title) for title in categories]
    tag_ids = [find_or_create_tag(title) for title in tags]
    return category_ids, tag_ids


def insert_post(post_data):
    result = posts_col.insert_one(post_data)
    return result.inserted_id


def read_and_process_markdown_files(dir):
    for filename in os.listdir(dir):
        if filename.endswith(".md"):
            filepath = os.path.join(dir, filename)
            with open(filepath, "r") as file:
                content = file.read()
                front_matter, markdown_content = content.split("---", 2)[1:]
                post_metadata = yaml.safe_load(front_matter)
                if "date" in post_metadata:
                    post_metadata["date"] = datetime.combine(post_metadata["date"], datetime.min.time())

                html_content = markdown2.markdown(
                    markdown_content, extras=["fenced-code-blocks", "highlightjs-lang", "toc"]
                )

                soup = BeautifulSoup(html_content, "html.parser")
                text_content = soup.get_text()
                preview = generate_preview(text_content)
                read_time = calculate_read_time(text_content)
                slug = generate_slug(post_metadata["title"])
                category_ids, tag_ids = process_categories_and_tags(post_metadata["categories"], post_metadata["tags"])
                post_document = {
                    "title": post_metadata["title"],
                    "date": post_metadata["date"],
                    "preview": preview,
                    "read_time": read_time,
                    "slug": slug,
                    "content": html_content,
                    "categories": category_ids,
                    "tags": tag_ids,
                }
                insert_post(post_document)


def main():
    clean_database()
    read_and_process_markdown_files(os.path.join(PROJECT_ROOT, "blog-posts"))
    print("inserted %d posts" % posts_col.count_documents({}))
    print("inserted %d categories" % categories_col.count_documents({}))
    print("inserted %d tags" % tags_col.count_documents({}))


if __name__ == "__main__":
    main()
