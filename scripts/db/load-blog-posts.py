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

# file: load-blog-posts.py
# date: 2024-01-30
# lang: python3
#
# load blog posts from markdown files into mongodb

import os
import re
import subprocess
import sys
from datetime import datetime

import markdown2
import pymongo
import yaml
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

PROJECT_ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config import config

CONFIG = config.parse()
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
        result = categories_col.insert_one({"title": title, "slug": title.lower().replace(" ", "-"), "post_count": 1})
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


def convert_images(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    img_tags = soup.find_all("img")

    if CONFIG["ENV"] == "development":
        base_url = f"http://{CONFIG['SERVER_NAME']}"
    else:
        base_url = f"https://{CONFIG['SERVER_NAME']}"

    figure_index = 1

    for img in img_tags:
        img_name = re.search(r"([^\/]+)(?=\.\w+$)", img["src"]).group(0)
        img_alt = img.get("alt", "")

        figure = soup.new_tag("figure")
        picture = soup.new_tag("picture")

        figure["id"] = f"figure-{figure_index}"

        source_webp = soup.new_tag("source", type="image/webp")
        source_webp["srcset"] = (
            f"{base_url}/assets/media/images/{img_name}-1920.webp 1920w, "
            f"{base_url}/assets/media/images/{img_name}-1600.webp 1600w, "
            f"{base_url}/assets/media/images/{img_name}-1366.webp 1366w, "
            f"{base_url}/assets/media/images/{img_name}-1024.webp 1024w, "
            f"{base_url}/assets/media/images/{img_name}-768.webp 768w, "
            f"{base_url}/assets/media/images/{img_name}-640.webp 640w"
        )
        picture.append(source_webp)

        source_jpeg = soup.new_tag("source", type="image/jpeg")
        source_jpeg["srcset"] = (
            f"{base_url}/assets/media/images/{img_name}-1920.jpg 1920w, "
            f"{base_url}/assets/media/images/{img_name}-1600.jpg 1600w, "
            f"{base_url}/assets/media/images/{img_name}-1366.jpg 1366w, "
            f"{base_url}/assets/media/images/{img_name}-1024.jpg 1024w, "
            f"{base_url}/assets/media/images/{img_name}-768.jpg 768w, "
            f"{base_url}/assets/media/images/{img_name}-640.jpg 640w"
        )
        picture.append(source_jpeg)

        new_img = soup.new_tag("img", src=f"/assets/media/images/{img_name}-640.jpg", alt=img_alt)

        picture.append(new_img)
        figure.append(picture)

        if img_alt:
            figcaption = soup.new_tag("figcaption")
            figcaption.string = f"Figure {figure_index}: {img_alt}"
            figure.append(figcaption)

        figure_index += 1

        img.replace_with(figure)
    return str(soup)


def apply_pygments(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    code_blocks = soup.find_all("code")
    for block in code_blocks:
        lang = None
        for class_ in block.get("class", []):
            if class_.startswith("language-"):
                lang = class_[len("language-") :]
                break

        if not lang:
            lang = "text"

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ValueError:
            lexer = get_lexer_by_name("text", stripall=True)

        formatter = HtmlFormatter(nowrap=True)
        highlighted_code = highlight(block.string, lexer, formatter)

        new_html = (
            f"<pre>"
            f'<code class="language-{lang}">'
            f"{highlighted_code}"
            f"</code>"
            f'<button title="Copy to clipboard">'
            f'<span aria-live="polite">Copy to clipboard</span>'
            f'<svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            f'<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>'
            f'<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>'
            f"</svg>"
            f"</button>"
            f"</pre>"
        )

        block.parent.replace_with(BeautifulSoup(new_html, "html.parser"))

    return str(soup)


def markdown_to_html(markdown_content):
    extras = ["fenced-code-blocks", "highlightjs-lang", "toc", "target-blank-links", "smarty-pants"]

    html_content = markdown2.markdown(
        markdown_content,
        extras=extras,
    )

    toc = html_content.toc_html

    html_content = convert_images(html_content)
    html_content = apply_pygments(html_content)

    return html_content, toc


def html_to_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


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

                html_content, toc = markdown_to_html(markdown_content)
                text_content = html_to_text(html_content)
                preview = generate_preview(text_content)
                read_time = calculate_read_time(text_content)
                slug = generate_slug(post_metadata["title"])
                category_ids, tag_ids = process_categories_and_tags(post_metadata["categories"], post_metadata["tags"])

                post_document = {
                    "title": post_metadata["title"],
                    "date": post_metadata["date"],
                    "image": post_metadata["image"],
                    "preview": preview,
                    "read_time": read_time,
                    "slug": slug,
                    "content": html_content,
                    "toc": toc,
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
