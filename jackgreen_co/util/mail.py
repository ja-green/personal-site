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

import requests
from flask import Flask, render_template


class Mail(object):
    def __init__(self: Self):
        pass

    def init_app(self: Self, app: Flask):
        self.endpoint = "https://api.postmarkapp.com/email"
        self.from_addr = app.config["MAIL_FROM"]
        self.mail_token = app.config["MAIL_TOKEN"]
        self.passthrough = False

        if not self.from_addr:
            if app.config["ENV"] == "development":
                self.passthrough = True
            else:
                raise ValueError("MAIL_FROM must be set in the app configuration.")
        if not self.mail_token:
            if app.config["ENV"] == "development":
                self.passthrough = True
            else:
                raise ValueError("MAIL_TOKEN must be set in the app configuration.")

    def send_email(self: Self, subject: str, body: str, to_addr: str) -> bool:
        if self.passthrough:
            return True

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": self.mail_token,
        }

        data = {
            "From": self.from_addr,
            "To": to_addr,
            "Subject": subject,
            "HtmlBody": body,
            "MessageStream": "outbound",
        }

        response = requests.post(self.endpoint, headers=headers, json=data)

        return response.status_code == 200


mail = Mail()


def send_email(subject: str, template: str, data: dict, to_addr: str) -> bool:
    body = render_template(template, data=data)

    return mail.send_email(subject, body, to_addr)
