const form = document.querySelectorAll("form#contact")[0];
const submit = form.querySelectorAll("button")[0];
const formFields = form.querySelectorAll("input:not([type=\"hidden\"]), select, textarea");

function checkValidity(e) {
    if (e.validity.valid) {
        setFormValid(e);
    } else {
        if (e.validity.valueMissing) {
            switch (e.id) {
                case "first-name":
                    m = "You need to enter a first name.";
                    break;
                case "last-name":
                    m = "You need to enter a last name.";
                    break;
                case "email":
                    m = "You need to enter an email address.";
                    break;
                case "message":
                    m = "You need to enter a message.";
            }
        } else if (e.validity.typeMismatch) {
            switch (e.id) {
                case "first-name":
                    m = "You need to enter a valid first name.";
                    break;
                case "last-name":
                    m = "You need to enter a valid last name.";
                    break;
                case "email":
                    m = "You need to enter a valid email address.";
                    break;
                case "message":
                    m = "You need to enter a valid message.";
            }
        } else if (e.validity.tooShort) {
            switch (e.id) {
                case "first-name":
                    m = `First name must be between ${e.minLength} and ${e.maxLength} characters long.`;
                    break;
                case "last-name":
                    m = `Last name must be between ${e.minLength} and ${e.maxLength} characters long.`;
                    break;
                case "email":
                    m = `Email must be between ${e.minLength} and ${e.maxLength} characters long.`;
                    break;
                case "message":
                    m = `Message must be between ${e.minLength} and ${e.maxLength} characters long.`;
            }
        }
        setFormInvalid(e, m);
    }
}

function setFormValid(element) {
    let feedbackElement = form.querySelectorAll("#" + element.id + "-error")[0];
    feedbackElement.textContent = "";
    feedbackElement.classList.add("invisible");
    element.classList.remove("invalid:[&:not(:focus)]:border-red-500");
    element.setAttribute("aria-invalid", false);

    let isFormValid = true;

    formFields.forEach(function(formElement) {
        if (!formElement.validity.valid) {
            isFormValid = false;
        }
    });

    if (isFormValid) {
        submit.disabled = false;
        submit.setAttribute("aria-disabled", false);
    } else {
        submit.disabled = true;
        submit.setAttribute("aria-disabled", true);
    }
}

function setFormInvalid(element, message) {
    element.classList.add("invalid:[&:not(:focus)]:border-red-500");
    element.setAttribute("aria-invalid", true);
    let feedbackElement = form.querySelectorAll("#" + element.id + "-error")[0];
    feedbackElement.textContent = message;
    feedbackElement.classList.remove("invisible");
    submit.disabled = true;
}

formFields.forEach(function(element) {
    element.addEventListener("input", function() {
        setFormValid(this);
    });
    element.addEventListener("blur", function() {
        checkValidity(this);
    });
});

form.setAttribute("novalidate", true);
submit.disabled = true;
submit.setAttribute("aria-disabled", "true");
