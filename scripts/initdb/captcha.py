#!/usr/bin/env python

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

import getopt
import json
import os
import subprocess
import sys
from datetime import datetime

import yaml
from bson import ObjectId

PROJECT_ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config import config

CONFIG = config.parse()


def report_fatal(msg, status=1):
    print(f"fatal: {msg}")
    sys.exit(status)


def parse_args():
    options = {}
    usage = "usage: build-captcha.py [-h|--help] [-i|--input <path>] [-o|--output <path>]"

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


def read_and_process_yaml_files(captcha_dir):
    challenges = []

    if not os.path.exists(captcha_dir):
        report_fatal(f"captcha directory '{captcha_dir}' does not exist")

    for filename in os.listdir(captcha_dir):
        if filename.endswith(".yaml"):
            locale = filename.split(".")[1]
            filepath = os.path.join(captcha_dir, filename)

            with open(filepath, "r") as file:
                content = yaml.safe_load(file)

            for category in content["categories"]:
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

                            challenge_document = {
                                "locale": locale,
                                "category": category["id"],
                                "question_id": question["id"],
                                "question_text": filled_template,
                                "answers": answers,
                            }

                            challenges.append(challenge_document)

    return challenges


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return {"$oid": str(o)}
        if isinstance(o, datetime):
            return {"$date": o.isoformat()}
        return json.JSONEncoder.default(self, o)


def main():
    options = parse_args()
    challenges = read_and_process_yaml_files(options["input"])

    output_file = os.path.join(options["output"], "initdb.js")

    if not os.path.exists(options["output"]):
        report_fatal(f"output directory '{options['output']}' does not exist")

    with open(output_file, "a") as f:
        f.write("db.captcha.drop();\n\n")

        f.write("db.captcha.insertMany(EJSON.deserialize([\n")
        for challenge in challenges:
            f.write(f"\t{json.dumps(challenge, cls=JSONEncoder)},\n")
        f.write("]));\n\n")

    print(f"inserted challenges into initdb.js ({len(challenges)} challenges)")


if __name__ == "__main__":
    main()
