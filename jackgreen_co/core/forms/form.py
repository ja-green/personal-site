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

from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    action = "/"

    def set_action(self, url):
        self.action = url

    @property
    def html_id(self):
        class_name = self.__class__.__name__
        if class_name.endswith("Form"):
            class_name = class_name[:-4]
        return class_name.lower()
