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

# file: captcha-questions.py
# date: 2024-01-30
# lang: python3
#
# apply substitutions to captcha questions and insert into mongodb

import os
import subprocess

import pymongo
import yaml

PROJECT_ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["jackgreen_co"]
captcha_col = db["captcha"]


def clean_database():
    captcha_col.delete_many({})


def insert_captcha_question(captcha_data):
    result = captcha_col.insert_one(captcha_data)
    return result.inserted_id


def load_questions_into_db(yaml_file, locale):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    for category in data["categories"]:
        for question in category["questions"]:
            for template in question["templates"]:
                for substitution_set in question["substitution_sets"]:
                    substitutions = substitution_set["substitutions"]
                    answers = substitution_set["answers"]
                    filled_template = template
                    for substitution in substitutions:
                        filled_template = filled_template.replace(
                            "{" + substitution["param"] + "}", substitution["value"]
                        )

                    question_document = {
                        "locale": locale,
                        "category": category["id"],
                        "question_id": question["id"],
                        "question_text": filled_template,
                        "answers": answers,
                    }

                    insert_captcha_question(question_document)


def read_and_process_captcha_files(dir):
    for file in os.listdir(dir):
        if file.endswith(".yaml"):
            locale = file.split(".")[1]
            load_questions_into_db(os.path.join(dir, file), locale)


def main():
    clean_database()
    read_and_process_captcha_files(os.path.join(PROJECT_ROOT, "captcha-data"))
    print("inserted %d questions" % captcha_col.count_documents({}))


if __name__ == "__main__":
    main()
