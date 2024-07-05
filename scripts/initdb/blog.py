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

# file: build-blog.py
# date: 2024-04-20
# lang: python3
#
# generate mongodb JSON import file from markdown blog posts

import getopt
import json
import os
import re
import subprocess
import sys
from datetime import datetime

import markdown2
import yaml
from bs4 import BeautifulSoup
from bson import ObjectId
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


def report_fatal(msg, status=1):
    print(f"fatal: {msg}")
    sys.exit(status)


def report_warning(msg):
    print(f"warning: {msg}")


def parse_args():
    options = {}
    usage = "usage: blog.py [-h|--help] [-i|--input <path>] [-o|--output <path>]"

    short_options = "hi:o:"
    long_options = ["help", "input=", "output="]

    try:
        opts, _ = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError as e:
        report_fatal(str(e))

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(usage)
            sys.exit()
        elif opt in ("-i", "--input"):
            options["input"] = arg
        elif opt in ("-o", "--output"):
            options["output"] = arg

    if options.get("input") is None or options.get("output") is None:
        print(usage)
        sys.exit(2)

    return options


def generate_slug(title):
    title = re.sub(r"[-_]+", " ", title)

    words = title.lower().split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    slug_base = " ".join(filtered_words)

    slug = re.sub(r"[\s]+", "-", slug_base)
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
        if block.parent.name != "pre":
            continue

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
    extras = [
        "fenced-code-blocks",
        "highlightjs-lang",
        "toc",
        "target-blank-links",
        "smarty-pants",
    ]

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


def generate_object_id():
    return ObjectId()


def read_series_metadata(filepath):
    with open(filepath, "r") as file:
        return yaml.safe_load(file.read())


def process_markdown_file(filepath, series_id, cats, tags):
    with open(filepath, "r") as file:
        content = file.read()
        front_matter, markdown_content = content.split("---", 2)[1:]
        post_metadata = yaml.safe_load(front_matter)

    cat_ids = [
        cats.setdefault(cat, {"id": generate_object_id(), "slug": generate_slug(cat)})["id"]
        for cat in post_metadata.get("categories", [])
    ]
    tag_ids = [
        tags.setdefault(tag, {"id": generate_object_id(), "slug": generate_slug(tag)})["id"]
        for tag in post_metadata.get("tags", [])
    ]

    html_content, toc = markdown_to_html(markdown_content)
    text_content = BeautifulSoup(html_content, "html.parser").get_text()
    preview = generate_preview(text_content)
    read_time = calculate_read_time(text_content)
    slug = generate_slug(post_metadata["title"])

    return {
        "_id": generate_object_id(),
        "title": post_metadata["title"],
        "date": datetime.combine(post_metadata["date"], datetime.min.time()),
        "series_index": post_metadata.get("series-index", 0),
        "image": post_metadata["image"],
        "preview": preview,
        "read_time": read_time,
        "slug": slug,
        "content": html_content,
        "toc": toc,
        "series": series_id,
        "categories": cat_ids,
        "tags": tag_ids,
    }


def read_and_process_markdown_files(blog_dir):
    posts = []
    series = {}
    categories = {}
    tags = {}

    if not os.path.exists(blog_dir):
        report_fatal(f"blog directory '{blog_dir}' does not exist")

    for dirname in os.listdir(blog_dir):
        dirpath = os.path.join(blog_dir, dirname)

        if dirpath.endswith(("/.git", "/drafts")):
            continue

        if not os.path.isdir(dirpath):
            continue

        index_path = os.path.join(dirpath, ".index")
        if not os.path.exists(index_path):
            report_warning(f"missing .index file in '{dirpath}'")
            continue

        series_metadata = read_series_metadata(index_path)
        series_id = series.setdefault(
            series_metadata["title"],
            {
                "id": generate_object_id(),
                "slug": generate_slug(series_metadata["title"]),
                "description": series_metadata["description"],
            },
        )["id"]

        for filename in os.listdir(dirpath):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(dirpath, filename)
            post_document = process_markdown_file(filepath, series_id, categories, tags)
            posts.append(post_document)

    return posts, series, categories, tags


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return {"$oid": str(o)}
        if isinstance(o, datetime):
            return {"$date": o.isoformat()}
        return json.JSONEncoder.default(self, o)


def main():
    options = parse_args()

    output_file = os.path.join(options["output"], "initdb.js")
    if not os.path.exists(options["output"]):
        report_fatal(f"output directory '{options['output']}' does not exist")

    with open(output_file, "w") as f:
        f.write("")

    posts, series, categories, tags = read_and_process_markdown_files(options["input"])

    with open(output_file, "a") as f:
        f.write("db.posts.drop();\n")
        f.write("db.series.drop();\n")
        f.write("db.categories.drop();\n")
        f.write("db.tags.drop();\n\n")

        f.write("db.posts.insertMany(EJSON.deserialize([\n")
        for post in posts:
            f.write(f"\t{json.dumps(post, cls=JSONEncoder)},\n")
        f.write("]));\n\n")

        f.write("db.series.insertMany(EJSON.deserialize([\n")
        for title, data in series.items():
            series_data = {
                "_id": ObjectId(data["id"]),
                "title": title,
                "slug": data["slug"],
                "description": data["description"],
            }
            f.write(f"\t{json.dumps(series_data, cls=JSONEncoder)},\n")
        f.write("]));\n\n")

        f.write("db.categories.insertMany(EJSON.deserialize([\n")
        for title, data in categories.items():
            category_data = {
                "_id": ObjectId(data["id"]),
                "title": title,
                "slug": data["slug"],
            }
            f.write(f"\t{json.dumps(category_data, cls=JSONEncoder)},\n")
        f.write("]));\n\n")

        f.write("db.tags.insertMany(EJSON.deserialize([\n")
        for title, data in tags.items():
            tag_data = {
                "_id": ObjectId(data["id"]),
                "title": title,
                "slug": data["slug"],
            }
            f.write(f"\t{json.dumps(tag_data, cls=JSONEncoder)},\n")
        f.write("]));\n")

    print(f"inserted posts into init-mongo.js ({len(posts)} posts)")
    print(f"inserted series into init-mongo.js ({len(series)} series)")
    print(f"inserted categories into init-mongo.js ({len(categories)} categories)")
    print(f"inserted tags into init-mongo.js ({len(tags)} tags)")


if __name__ == "__main__":
    main()
