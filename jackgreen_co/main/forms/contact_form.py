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

from wtforms import validators as wtforms_validators

from jackgreen_co.core.forms import fields, form, meta, validators
from jackgreen_co.main.messages import Messages


class ContactForm(form.BaseForm):
    class Meta(meta.AutoMeta):
        csrf = False

    first_name = fields.StringField(
        label=Messages.main_contact_form_firstname_label,
        validators=[
            wtforms_validators.DataRequired(Messages.main_contact_form_firstname_required),
            wtforms_validators.Length(min=2, max=30, message=Messages.main_contact_form_firstname_length),
        ],
    )

    last_name = fields.StringField(
        label=Messages.main_contact_form_lastname_label,
        validators=[
            wtforms_validators.DataRequired(Messages.main_contact_form_lastname_required),
            wtforms_validators.Length(min=2, max=30, message=Messages.main_contact_form_lastname_length),
        ],
    )

    email = fields.EmailField(
        label=Messages.main_contact_form_email_label,
        validators=[
            wtforms_validators.DataRequired(Messages.main_contact_form_email_required),
            wtforms_validators.Length(min=4, message=Messages.main_contact_form_email_length),
            wtforms_validators.Email(
                message=Messages.main_contact_form_email_invalid,
                granular_message=True,
                check_deliverability=True,
            ),
        ],
    )

    message = fields.TextAreaField(
        label=Messages.main_contact_form_message_label,
        validators=[
            wtforms_validators.DataRequired(Messages.main_contact_form_message_required),
            wtforms_validators.Length(min=1, max=2000, message=Messages.main_contact_form_message_length),
        ],
    )

    captcha = fields.CaptchaField(
        validators=[
            wtforms_validators.DataRequired(Messages.main_contact_form_captcha_required),
            validators.CaptchaValidator(Messages.main_contact_form_captcha_invalid),
        ],
    )

    age_token = fields.AgeTokenField(
        validators=[
            validators.AgeTokenValidator(Messages.main_contact_form_agetoken_invalid),
        ],
    )
