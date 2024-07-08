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

from __future__ import absolute_import, unicode_literals

from typing import Self

from wtforms import Field
from wtforms.fields.core import UnboundField
from wtforms.meta import DefaultMeta
from wtforms.validators import Length, NumberRange

MINMAX_VALIDATORS = (NumberRange,)
MINMAXLENGTH_VALIDATORS = (Length,)


def set_required(field: Field, render_kw: dict = None, force: bool = False) -> dict:
    if render_kw is None:
        render_kw = {}
    if "required" in render_kw and not force:
        return render_kw
    if field.flags.required:
        render_kw["required"] = True
    return render_kw


def set_invalid(field: Field, render_kw: dict = None) -> dict:
    if render_kw is None:
        render_kw = {}
    if field.errors:
        classes = render_kw.get("class") or render_kw.pop("class_", "")
        if classes:
            render_kw["class"] = "invalid {}".format(classes)
        else:
            render_kw["class"] = "invalid"
    return render_kw


def set_minmax(field: Field, render_kw: dict = None, force: bool = False) -> dict:
    if render_kw is None:
        render_kw = {}
    for validator in field.validators:
        if isinstance(validator, MINMAX_VALIDATORS):
            if "min" not in render_kw or force:
                v_min = getattr(validator, "min", -1)
                if v_min not in (-1, None):
                    render_kw["min"] = v_min
            if "max" not in render_kw or force:
                v_max = getattr(validator, "max", -1)
                if v_max not in (-1, None):
                    render_kw["max"] = v_max
    return render_kw


def set_minmaxlength(field: Field, render_kw: dict = None, force: bool = False) -> dict:
    if render_kw is None:
        render_kw = {}
    for validator in field.validators:
        if isinstance(validator, MINMAXLENGTH_VALIDATORS):
            if "minlength" not in render_kw or force:
                v_min = getattr(validator, "min", -1)
                if v_min not in (-1, None):
                    render_kw["minlength"] = v_min
            if "maxlength" not in render_kw or force:
                v_max = getattr(validator, "max", -1)
                if v_max not in (-1, None):
                    render_kw["maxlength"] = v_max
    return render_kw


def set_title(field: Field, render_kw: dict = None) -> dict:
    if render_kw is None:
        render_kw = {}
    if "title" not in render_kw and getattr(field, "description"):
        render_kw["title"] = "{}".format(field.description)
    return render_kw


def get_html5_kwargs(field: Field, render_kw: dict = None, force: bool = False) -> dict:
    if isinstance(field, UnboundField):
        msg = "This function needs a bound field not: {}"
        raise ValueError(msg.format(field))
    kwargs = render_kw.copy() if render_kw else {}
    kwargs = set_required(field, kwargs, force)
    kwargs = set_invalid(field, kwargs)
    kwargs = set_minmax(field, kwargs, force)
    kwargs = set_minmaxlength(field, kwargs, force)
    kwargs = set_title(field, kwargs)
    return kwargs


class AutoMeta(DefaultMeta):
    def render_field(self: Self, field: Field, render_kw: dict = None) -> str:
        field_kw = getattr(field, "render_kw", None)
        if field_kw is not None:
            render_kw = dict(field_kw, **render_kw)
        render_kw = get_html5_kwargs(field, render_kw)
        return field.widget(field, **render_kw)
