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

from flask import current_app, flash, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue

from jackgreen_co.main import main, messages
from jackgreen_co.main.forms import contact_form
from jackgreen_co.util import mail


@main.route("/")
def index() -> ResponseReturnValue:
    return render_template("main/index.jinja.html")


@main.route("/about")
def about() -> str:
    return render_template("main/about.jinja.html")


@main.route("/contact", methods=["POST", "GET"])
def contact() -> ResponseReturnValue:
    form = contact_form.ContactForm(request.form)
    form.set_action(url_for("main.contact"))

    if form.validate_on_submit():
        data = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "email": form.email.data,
            "message": form.message.data,
        }

        mail_sent = mail.send_email(
            messages.Messages.main_contact_submitted_email_subject,
            "email/contact-form-submission.jinja.html",
            data,
            current_app.config["MAIL_TO"],
        )

        if mail_sent:
            flash(messages.Messages.main_contact_submitted_success_message % (form.first_name.data.title()), "success")
        else:
            flash(messages.Messages.main_contact_submitted_error_message % (form.first_name.data.title()), "error")

        return redirect(url_for("main.contact"), 303)
    return render_template("main/contact.jinja.html", contact_form=form)


@main.route("/email")
def email() -> ResponseReturnValue:
    return render_template("main/email.jinja.html")


@main.route("/privacy-policy")
def privacy() -> ResponseReturnValue:
    return render_template("main/privacy.jinja.html")
