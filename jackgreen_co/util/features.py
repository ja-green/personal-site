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


class FeatureFlags(object):
    pass


class FeatureFlagsDev(FeatureFlags):
    pass


class FeatureFlagsProd(FeatureFlags):
    pass


class Features(object):
    def __init__(self):
        pass

    def parse_feature_flags(self, obj):
        flags = {}
        for key in dir(obj):
            if key.isupper():
                flags[key] = getattr(obj, key)
        return flags

    def init_app(self, app):
        if app.config["ENV"] == "development":
            flags = self.parse_feature_flags(FeatureFlagsDev)
        else:
            flags = self.parse_feature_flags(FeatureFlagsProd)
        app.features = flags


features = Features()
