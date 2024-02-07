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
    main_contact_lead = "Feel free to contact me via email, my GPG key can be found here. Alternatively, you can use the form below and I'll get back to you as soon as I can."
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
