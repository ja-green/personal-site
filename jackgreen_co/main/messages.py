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

from jackgreen_co.core import messages


class Messages(messages.Messages):
    main_index_description = "TODO: Add a description here."
    main_index_heading = "Hi there, I'm Jack."
    main_index_subheading = "Cyber Security Consultant, developer and life-long learner."
    main_index_button1 = "View my blog"
    main_index_button2 = "See more about me"

    main_about_heading = "About"
    main_about_subheading = "A bit about me."
    main_about_description = "TODO: Add a description here."

    main_contact_heading = "Contact"
    main_contact_subheading = "Get in touch."
    main_contact_description = "TODO: Add a description here."
    main_contact_lead1 = "Feel free to contact me via email; my email details and PGP key can be found "
    main_contact_lead2 = ". Alternatively, you can use the form below and I'll get back to you as soon as I can."
    main_contact_form_captcha_lead = "Please enter the following CAPTCHA to verify that you are not a robot."
    main_contact_form_firstname_label = "First Name"
    main_contact_form_firstname_required = "You need to enter a first name."
    main_contact_form_firstname_length = "First name must be between 2 and 30 characters long."
    main_contact_form_lastname_label = "Last Name"
    main_contact_form_lastname_required = "You need to enter a last name."
    main_contact_form_lastname_length = "Last name must be between 2 and 30 characters long."
    main_contact_form_email_label = "Email"
    main_contact_form_email_required = "You need to enter an email address."
    main_contact_form_email_length = "Email must be at least 4 characters long."
    main_contact_form_email_invalid = "You need to enter a valid email address."
    main_contact_form_message_label = "Message"
    main_contact_form_message_required = "You need to enter a message."
    main_contact_form_message_length = "Message must be between 1 and 300 characters long."
    main_contact_form_captcha_label = "Challenge"
    main_contact_form_captcha_required = "Please verify that you are not a robot."
    main_contact_form_captcha_invalid = "Please verify that you are not a robot."
    main_contact_form_agetoken_invalid = "Please wait a moment before submitting the form again."
    main_contact_form_submit = "Submit"
    main_contact_submitted = "Thanks %s, your message has been sent successfully"

    main_email_heading = "Email"
    main_email_subheading = "Send me an encrypted email."
    main_email_description = "TODO: Add a description here."
    main_email_lead = "If you prefer to communicate securely via encrypted email rather than using the contact form, my PGP public key is available below. Feel free to import it to your keyring and use it for any encrypted correspondence."
    main_email_pgp_key = """-----BEGIN PGP PUBLIC KEY BLOCK-----

xjMEYf7BUhYJKwYBBAHaRw8BAQdAqiwuBg9rN/NQMrV7G8lpWGJztFwuBBUU
weoCW/jzdHLNJWphY2tAamFja2dyZWVuLmNvIDxqYWNrQGphY2tncmVlbi5j
bz7CjwQQFgoAIAUCYf7BUgYLCQcIAwIEFQgKAgQWAgEAAhkBAhsDAh4BACEJ
EEJ/7p7hQ1DtFiEESH63f8TdR7d7VFBrQn/unuFDUO0BPQD/WAnrSlLnNfRF
e+RGwbWXgG/LPUAH6QqHnFZiCCkqQG0A/2RxOdmlvVSy8gqMAVrGtMoZ58S4
I8WCQmK1ieziTR8AzjgEYf7BUhIKKwYBBAGXVQEFAQEHQKF7voPviKyhc/nu
mYG7SPB1mwtL4MxJtc9ITaOUNSZbAwEIB8J4BBgWCAAJBQJh/sFSAhsMACEJ
EEJ/7p7hQ1DtFiEESH63f8TdR7d7VFBrQn/unuFDUO1a+wD/VCuOU12ryqj1
WxBXZkwdDIl7P/6hQrnWP6ilnWnKaTwA/02NnastGj26k7qMv17pPz1+fxRH
RhT3NUn60/4WXHUD
=4kLj
-----END PGP PUBLIC KEY BLOCK-----"""
    main_email_pgp_fingerprint_lead = "Fingerprint:"
    main_email_pgp_fingerprint = "487eb77fc4dd47b77b54506b427fee9ee14350ed"
    main_email_address_lead = "All emails can be directed to:"
    main_email_address = "jack at jackgreen dot co"
