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

import time
from typing import Self

from flask import session
from wtforms import Field, Form
from wtforms.validators import ValidationError


class CaptchaValidator(object):
    def __init__(self: Self, message: str = None):
        if not message:
            message = "Please verify that you are not a robot."
        self.message = message

    def __call__(self: Self, form: Form, field: Field):
        del session["captcha-answers"]

        captcha_answer = field.data.lower()
        if not field._answers:
            raise ValidationError(field.gettext(self.message))

        valid_answers = [answer.lower() for answer in field._answers]

        if not captcha_answer or captcha_answer not in valid_answers:
            raise ValidationError(field.gettext(self.message))


class AgeTokenValidator(object):
    def __init__(self: Self, message: str = None, min_age: int = 60):
        if not message:
            message = "Please wait before submitting the form again."
        self.message = message
        self.min_age = min_age

    def __call__(self: Self, form: Form, field: Field):
        del session["age-token"]
        del session["age-token-timestamp"]

        response_token = field.data
        if not field._token or not response_token:
            raise ValidationError(field.gettext(self.message))

        age = time.time() - float(field._timestamp)

        if response_token != field._token or age < self.min_age:
            raise ValidationError(field.gettext(self.message))
