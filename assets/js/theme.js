document.addEventListener("DOMContentLoaded", function() {
    const darkModeButton = document.getElementById("dark-mode-toggle");

    function setThemeCookie(theme) {
        const expiration = new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toUTCString();
        document.cookie = `theme=${theme}; path=/; expires=${expiration}; domain=jackgreen.co; SameSite=Lax`;
    }

    if (darkModeButton) {
        darkModeButton.classList.remove("hidden");

        darkModeButton.addEventListener("click", function() {
            const isDarkMode = document.documentElement.classList.toggle("dark");
            setThemeCookie(isDarkMode ? "dark" : "light");
        });
    }
});
