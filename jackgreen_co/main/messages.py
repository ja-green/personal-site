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

from jackgreen_co.core import messages


class Messages(messages.Messages):
    main_index_description = "Welcome to Jack Green's personal website and blog. Explore articles on tech, security, personal interests, and more. Join me in my passion for self-development and education."
    main_index_heading = "Hi there, I'm Jack."
    main_index_subheading = "Discover my open-source projects, philosophy, and joy of perpetual learning."
    main_index_button1 = "View my blog"
    main_index_button2 = "See more about me"

    main_about_title = "About"
    main_about_heading = "About"
    main_about_subheading = "A bit about me and this site."
    main_about_description = "Learn more about Jack Green, a passionate tech enthusiast and educator. Discover my journey, interests, and the motivation behind my blog posts."
    main_about_personal_p1 = "Welcome to my personal website! Here, I combine my enthusiasm for free and open-source software with my love for programming. This site serves as a platform for sharing my projects, thoughts, and interests, aiming to provide an educational and inspiring space for like-minded individuals."
    main_about_personal_p2 = "Stoicism greatly influences my approach to life, emphasising the importance of focusing on what we can control, cultivating inner strength and resilience, and striving for continuous self-improvement. These values are deeply integrated into the content you’ll discover here, reflecting both my personal journey and professional endeavours."
    main_about_personal_p3 = "Programming is a core part of my life. I enjoy working on a variety of open-source projects, ranging from command-line tools to technical tutorials and website development. My projects are constantly evolving, and I plan to share details about them here."
    main_about_personal_p4 = "This website is designed to be more than just a blog; It’s a dynamic space where I nurture and share my ideas. You’ll find a diverse array of content, including articles on philosophy, detailed walkthroughs and tutorials, updates on my latest projects, and reflections on various topics that interest me. My aim is to inspire, educate, and provide valuable insights to my readers."
    main_about_personal_p5_1 = "Feel free to explore the site, and if you have any questions or just want to connect, there’s a contact form available"
    main_about_personal_p5_2 = (
        "For secure communication, you can also reach me via email using my PGP key, of which the details can be found"
    )
    main_about_personal_p6 = "Thank you for visiting! I hope you find something here that piques your interest or helps you on your personal or professional journey."
    main_about_tech_heading = "Technical Details"
    main_about_tech_p1 = "This website is not just a platform for sharing content; it is also a showcase of the technologies and principles I advocate for. Here are some details about the technical implementation of the site:"
    main_about_tech_p2 = "The site is built using Python with the Flask framework, utilising Jinja2 for templating. The frontend is written in HTML5 and uses Tailwind CSS for styling. I use as minimal JavaScript as possible to support text-based browsers and users blocking JavaScript; there is no essential functionality on this site that requires JavaScript."
    main_about_tech_p3 = "The site is containerised with Docker and managed using docker-compose. The services, including the Flask application, a MongoDB database, a Redis instance used for caching and storing session data, and nginx as the web server acting as a reverse proxy, are hosted on a CentOS VPS with SELinux. All services communicate internally via mutual TLS. Additionally, there is a service that obtains and renews Let's Encrypt SSL certificates and stores the OCSP response for stapling."
    main_about_tech_p4_1 = "The source code for this website is open-source and available on GitHub under the"
    main_about_tech_p4_2 = "The content is licensed under the"
    main_about_tech_p4_3 = "The code repository is available"

    main_contact_title = "Contact"
    main_contact_heading = "Contact"
    main_contact_subheading = "Get in touch."
    main_contact_description = "Get in touch with me. Reach out for enquiries, feedback, or just to connect. I'm here to engage with readers of my posts."
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
    main_contact_submitted_email_subject = "New Contact Form Submission"
    main_contact_submitted_success_heading = "Message Sent"
    main_contact_submitted_success_message = "Thanks %s, your message has been sent successfully."
    main_contact_submitted_error_heading = "Message Not Sent"
    main_contact_submitted_error_message = "Sorry %s, your message could not be sent. Please try again later."

    main_email_title = "Email"
    main_email_heading = "Email"
    main_email_subheading = "Send me an encrypted email."
    main_email_description = (
        "Send me an encrypted email using my PGP public key. I'd love to communicate securely with you."
    )
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

    main_privacy_title = "Privacy Policy"
    main_privacy_heading = "Privacy Policy"
    main_privacy_subheading = "Your privacy is important."
    main_privacy_description = "Learn about how I collect, use, and protect your personal information when you use my website. I am committed to safeguarding your privacy and handling your data in an open and transparent manner."
    main_privacy_date = "Effective date:"
    main_privacy_lead = "I am committed to protecting your privacy and handling your data in an open and transparent manner. This privacy policy sets out how I collect, use, store, and protect your personal information when you use my website."
    main_privacy_q1 = "What information do I collect?"
    main_privacy_a1 = "I collect information from you only when you voluntarily fill out the contact form on my website. The information collected includes your first name, last name, and email address. You may visit my website without providing any personal information, and no personal information will be gathered from you unless you provide it. No sensitive information is collected from you during any use of my website. I retain server logs which include the IP address of every request to my server(s), but I anonymise these IP addresses to protect your privacy."
    main_privacy_q2 = "How do I use your information?"
    main_privacy_a2 = "Any of the information I collect from you may be used in one of the following ways:"
    main_privacy_a2_list1_title = "To improve my site:"
    main_privacy_a2_list1_info = (
        "I continually strive to improve my site offerings based on the information and feedback I receive from you."
    )
    main_privacy_a2_list2_title = "To communicate with you:"
    main_privacy_a2_list2_info = (
        "The email address you provide may be used respond to your inquiries, requests or questions."
    )
    main_privacy_a2_list3_title = "To maintain security:"
    main_privacy_a2_list3_info = "Server logs are used to monitor and maintain the security of my website, analyse performance, troubleshoot issues, and detect and prevent malicious activity."
    main_privacy_q3 = "How do I protect your information?"
    main_privacy_a3 = "I implement a variety of security measures to maintain the safety of your personal information when you enter, submit, or access your personal information. I collect only the minimum amount of information necessary for the website to function and for me to address any issues. Access to your personal data is limited to just myself. I employ security measures to protect your information and keep my systems up-to-date."
    main_privacy_q4 = "What is my data retention policy?"
    main_privacy_a4_p1 = "I retain the personal information you provide in the contact form only for as long as necessary to respond to your inquiry or resolve your issue. Once the enquiry/conversation has completed, the communication will be deleted and no personal data will be stored for future use."
    main_privacy_a4_p2 = "Server logs are retained for a period of 7 days, after which they are automatically deleted. After 24 hours, any IP addresses stored in the logs are automatically anonymized to SHA-256 hashes with a randomly generated salt that rotates daily."
    main_privacy_q5 = "Do I use cookies?"
    main_privacy_a5 = 'Yes, but only a single session cookie (named "session" if you\'d like to inspect it yourself). Session cookies are temporary and are automatically deleted after the browser session ends. These cookies help me understand and save your preferences for your current session, for example, your preference of light-mode or dark-mode.'
    main_privacy_q6 = "Do I disclose any information to outside parties?"
    main_privacy_a6 = "No, I do not sell, trade, or transfer any of your information to outside parties. I may release information when necessary to comply with the law, enforce my policies, or protect my or others’ rights, property, or safety."
    main_privacy_q7 = "Third-party links"
    main_privacy_a7 = "My website may include or link to third-party products or services. These third parties have separate and independent privacy policies, and I have no responsibility or liability for their content or activities."
    main_privacy_q8 = "Children's Online Privacy Protection Act compliance"
    main_privacy_a8 = "My website is intended for use by individuals who are at least 13 years old. If you are under 13, please do not use this website. If I discover that personal information from a child under 13 has been collected, I will delete it promptly."
    main_privacy_q9 = "Online Privacy Policy only"
    main_privacy_a9 = "This online privacy policy applies only to information collected through my website and not to information collected offline."
    main_privacy_q10 = "Your consent"
    main_privacy_a10 = "By using my site, you consent to this privacy policy."
    main_privacy_q11 = "Changes to my privacy policy"
    main_privacy_a11 = "I may update this privacy policy from time to time. Any changes will be posted on this page with an updated effective date. Significant changes will be communicated through an announcement on the homepage."
    main_privacy_close1_1 = "This document is licensed under the"
    main_privacy_close1_2 = "and was last updated on"
    main_privacy_close2_1 = (
        "For any questions or concerns regarding this privacy policy, please contact me using the contact form"
    )
    main_privacy_close2_2 = "or via email, of which the details can be found"
