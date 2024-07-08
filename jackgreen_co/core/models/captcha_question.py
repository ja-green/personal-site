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

from typing import Self


class CaptchaQuestion(object):
    def __init__(
        self: Self, object_id: str, locale: str, category: str, question_id: str, question_text: str, answers: list
    ):
        self._object_id = object_id
        self._locale = locale
        self._category = category
        self._question_id = question_id
        self._question_text = question_text
        self._answers = answers

    @property
    def object_id(self: Self) -> str:
        return self._object_id

    @property
    def locale(self: Self) -> str:
        return self._locale

    @property
    def category(self: Self) -> str:
        return self._category

    @property
    def question_id(self: Self) -> str:
        return self._question_id

    @property
    def question_text(self: Self) -> str:
        return self._question_text

    @property
    def answers(self: Self) -> list:
        return self._answers

    def __repr__(self: Self) -> str:
        return "<CaptchaQuestion %s>" % self.question_id
