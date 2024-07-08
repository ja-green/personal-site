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

import secrets
import time
from typing import Self

from flask import session
from wtforms import HiddenField, widgets
from wtforms import StringField as WTFStringField
from wtforms import TextAreaField as WTFTextAreaField
from wtforms.fields import EmailField as WTFEmailField

from jackgreen_co.core.services import captcha_service


class HyphenatedNameMixin:
    _hyphenated_name = None

    def __getattr__(self: Self, name: str) -> str:
        if name == "name" and self._hyphenated_name:
            return self._hyphenated_name
        return super().__getattr__(name)

    def __setattr__(self: Self, name: str, value: str):
        if name == "name":
            self._hyphenated_name = value.replace("_", "-")
        else:
            super().__setattr__(name, value)


class StringField(HyphenatedNameMixin, WTFStringField):
    pass


class TextAreaField(HyphenatedNameMixin, WTFTextAreaField):
    pass


class EmailField(HyphenatedNameMixin, WTFEmailField):
    pass


class AgeTokenField(HyphenatedNameMixin, HiddenField):
    widget = widgets.HiddenInput()

    def __init__(self: Self, label: str = None, validators: list = None, **kwargs: dict):
        super(AgeTokenField, self).__init__(label, validators=validators, **kwargs)

        if not kwargs["_form"].is_submitted():
            token = secrets.token_hex(64)
            timestamp = time.time()

            session["age-token"] = token
            session["age-token-timestamp"] = timestamp

            self._token = token
            self._timestamp = timestamp
        else:
            self._token = session.get("age-token", None)
            self._timestamp = session.get("age-token-timestamp", None)

    def _value(self: Self) -> str:
        return self._token


class CaptchaField(StringField):
    widget = widgets.TextInput()

    def __init__(self: Self, validators: list = None, **kwargs: dict):
        super(CaptchaField, self).__init__(label=None, validators=validators, **kwargs)

        if not kwargs["_form"].is_submitted():
            question = captcha_service.get_random()

            if not question:
                raise RuntimeError("No questions found in the database.")

            session["captcha-answers"] = question.answers

            self._answers = question.answers
            self.label.text = question.question_text
        else:
            self._answers = session.get("captcha-answers", [])
