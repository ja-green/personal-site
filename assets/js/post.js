const animateButtonSuccess = (button) => {
    button.innerHTML =
        "<span aria-live=\"polite\">Copied</span><svg aria-hidden=\"true\" xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><polyline points=\"20 6 9 17 4 12\"></polyline></svg>";
    setTimeout(() => {
        button.innerHTML =
            "<span aria-live=\"polite\">Copy to clipboard</span><svg aria-hidden=\"true\" xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"9\" y=\"9\" width=\"13\" height=\"13\" rx=\"2\" ry=\"2\"></rect><path d=\"M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1\"></path></svg>";
    }, 2000);
};

const animateButtonFailure = (button) => {
    button.innerHTML =
        "<span aria-live=\"polite\">Copy failed</span><svg aria-hidden=\"true\" xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><line x1=\"18\" y1=\"6\" x2=\"6\" y2=\"18\"></line><line x1=\"6\" y1=\"6\" x2=\"18\" y2=\"18\"></line></svg>";
    setTimeout(() => {
        button.innerHTML =
            "<span aria-live=\"polite\">Copy to clipboard</span><svg aria-hidden=\"true\" xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"9\" y=\"9\" width=\"13\" height=\"13\" rx=\"2\" ry=\"2\"></rect><path d=\"M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1\"></path></svg>";
    }, 2000);
};

document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelectorAll("pre > button").forEach(button => {
        button.style.display = "inline-flex";
        button.addEventListener("click", function(e) {
            e.preventDefault();
            const codeBlock = this.previousElementSibling.textContent;

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(codeBlock).then(() => {
                    animateButtonSuccess(this);
                }).catch((e) => {
                    fallbackCopyTextToClipboard(codeBlock, this);
                });
            } else {
                fallbackCopyTextToClipboard(codeBlock, this);
            }
        });
    });
});

function fallbackCopyTextToClipboard(text, button) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    try {
        const successful = document.execCommand("copy");
        if (successful) {
            animateButtonSuccess(button);
        }
    } catch (e) {
        animateButtonFailure(button);
    } finally {
        document.body.removeChild(textarea);
    }
}
