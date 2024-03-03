document.addEventListener("DOMContentLoaded", function() {
    const darkModeButton = document.getElementById("dark-mode-toggle");

    function setThemeCookie(theme) {
        const expiration = new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toUTCString();
        document.cookie = `theme=${theme}; path=/; expires=${expiration}; domain=jackgreen.co; SameSite=Lax`;
    }

    function updateImageSources(isDarkMode) {
        const darkThemeSources = document.querySelectorAll("source[data-theme=\"dark\"]");
        const lightThemeSources = document.querySelectorAll("source[data-theme=\"light\"]");

        if (isDarkMode) {
            darkThemeSources.forEach(source => source.media = "(min-width: 0px)");
            lightThemeSources.forEach(source => source.media = "not all");
        } else {
            darkThemeSources.forEach(source => source.media = "not all");
            lightThemeSources.forEach(source => source.media = "(min-width: 0px)");
        }
    }

    if (darkModeButton) {
        darkModeButton.classList.remove("hidden");

        darkModeButton.addEventListener("click", function() {
            const isDarkMode = document.documentElement.classList.toggle("dark");
            updateImageSources(isDarkMode);
            setThemeCookie(isDarkMode ? "dark" : "light");
        });
    }
});
