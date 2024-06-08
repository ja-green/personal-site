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

from jackgreen_co import core
from jackgreen_co.core.models import captcha_question


def get(data: dict = None) -> list:
    question_data = core.db.captcha.find(data)

    return [
        captcha_question.CaptchaQuestion(
            object_id=q.get("_id"),
            locale=q.get("locale"),
            category=q.get("category"),
            question_id=q.get("question_id"),
            question_text=q.get("question_text"),
            answers=q.get("answers"),
        )
        for q in question_data
    ]


def get_random(data: dict = None) -> captcha_question.CaptchaQuestion:
    match = [{"$match": data}] if data else []

    terms = match + [{"$sample": {"size": 1}}]
    question_data = core.db.captcha.aggregate(terms)

    for q in question_data:
        return captcha_question.CaptchaQuestion(
            object_id=q.get("_id"),
            locale=q.get("locale"),
            category=q.get("category"),
            question_id=q.get("question_id"),
            question_text=q.get("question_text"),
            answers=q.get("answers"),
        )

    return None
