PWeb.viewMode = (function () {

    let icon = jQuery("#switch-mode")

    function setDarkMode() {
        localStorage.setItem('mode', 'dark')
        let body = jQuery("body")
        if (!body.hasClass("dark")) {
            body.addClass("dark")
        }
        icon.html("");
        icon.html('<i class="fa-solid fa-moon"></i>')
    }

    function removeDarkMode() {
        jQuery("body").removeClass("dark")
        localStorage.removeItem('mode')
        icon.html("");
        icon.html('<i class="fa-solid fa-sun"></i>')
    }

    return {
        init: function () {
            let checkBox = jQuery("#switch-mode")
            let currentMode = localStorage.getItem("mode")
            if (currentMode === "dark") {
                setDarkMode()
            }

            checkBox.on("click", function () {
                currentMode = localStorage.getItem("mode")
                if (!currentMode) {
                    setDarkMode()
                } else {
                    removeDarkMode()
                }
            })
        }
    }
}());