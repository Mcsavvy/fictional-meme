var main = {
    darkmodeCss: "<link id='dm' href='/static/css/dark-mode.css' rel='stylesheet'/>",
    lightmodeCss: "<link id='lm' href='/static/css/light-mode.css' rel='stylesheet'/>",
    // Create cookie
    createCookie: function(name, value, days) {
        var expires;
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
        }
        else {
            expires = "";
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    },

    // Read cookie
    readCookie: function(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(";");
        for(var i=0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) === " ") {
                c = c.substring(1, c.length);
            }
            if (c.indexOf(nameEQ) === 0) {
                return c.substring(nameEQ.length,c.length);
            }
        }
        return null;
    },

    // Erase cookie
    eraseCookie: function(name) {
        this.createCookie(name, "", -1);
    },

    // Toggle light/dark mode 
    toggleDarkMode: function() {
        if ($('#dm').length == 0) {
            $("#lm").remove();
            $("head:first").append($(this.darkmodeCss));
            this.createCookie("preferredTheme", "dark-mode", 365);
        } else {
            $("#dm").remove();
            $("head:first").append($(this.lightmodeCss));
            this.createCookie("preferredTheme", "light-mode", 365);
        }
    },

    // Get preferred mode
    getPreferredMode: function() {
        if (this.readCookie("preferredTheme")) {
            return this.readCookie("preferredTheme");
        } else {
            return "not-set";
        }
    },
    setPrefferedMode: function() {
        mode = this.getPreferredMode();
        if (mode == 'not-set'){
            $("head:first").append($(this.lightmodeCss));
            this.createCookie("preferredTheme", "light-mode", 365);
        } else if (mode == 'light-mode'){
            $('#dm').remove()
            $("head:first").append($(this.lightmodeCss));
        } else if (mode == 'dark-mode'){
            $('#lm').remove()
            $("head:first").append($(this.darkmodeCss));
        }
    }
}
