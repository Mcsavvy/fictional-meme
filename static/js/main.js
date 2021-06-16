let ajx = {
    post: {
        ajax: 1,
        type: "POST"
    },
    get: {
        ajax: 1,
        type: "GET"
    }
}

function toast(text, type, timeout, callback, position) {
    VanillaToasts.create({
        // notification message
        text: text,

        // success, info, warning, error   / optional parameter
        type: type || 'info',

        // topRight, topLeft, topCenter, bottomRight, bottomLeft, bottomCenter
        positionClass: position || 'bottomRight',

        // auto dismiss after 5000ms
        timeout: timeout || 2000,

        // executed when toast is clicked
        callback: callback || null

    });
}

function isNone(obj) {
    if ((typeof obj == typeof undefined || Boolean(obj) == false)) {
        return true
    } else {
        return false
    }

}

function message(text, type) {
    toast(text, type, 4000, function() {}, "topRight")
}

// JavaScript function to get cookie by name; retrieved from https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// JavaScript wrapper function to send HTTP requests using Django's "X-CSRFToken" request header
request = {
    get: function(path, body, callback) {
        if (isNone(body)){
            body = new Object
        }
        body = {...body, ...ajx.get}
        $.ajax({
        	url: path,
        	type: "GET",
        	data: body,
        	headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
        	success: callback
        })
    },
    post: function(path, body, callback) {
        if (isNone(body)){
            body = new Object
        }
        body = {...body, ...ajx.get}
        $.ajax({
            url: path,
            type: "POST",
            data: body,
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            success: callback
        })
    }
}

function dispatchEvent(events_args){
    $.ajax({
        url: '/api/events',
        type: "GET",
        headers: {
            "X-Events": events_args,
            "X-Ajax": 1
        },
    })
}

function addToCart(self) {
    request.get($(self).attr('url'), null, function(data) {
        request.get("/shop", null, function(data){
        	shop.updateCart(data.cart)
        	shop.updateWishlist(data.wish)
        	shop.updateNotification(data.notification)
        })
        card = $(self).closest('.product-card')
        card.load(`?x-ajax #${card.attr('id')} .ajax-wrapper`)
        toast(data.message, data.level, 2000, null)
    })
}

function addToWishlist(self) {
    request.get($(self).attr('url'), null, function(data) {
        request.get("/shop", null, function(data){
        	shop.updateCart(data.cart)
        	shop.updateWishlist(data.wish)
        	shop.updateNotification(data.notification)
        })
        card = $(self).closest('.product-card')
        card.load(`?x-ajax #${card.attr('id')} .ajax-wrapper`)
        toast(data.message, data.level, 2000, null)
    })
}

function lightMode(){
	request.post(
		"/theme",
		{"dm": 0},
		function(data) {
			if ("message" in data){
				toast(
					data.message,
					data.level,
					1000,
					$("#theme-control").load(" #theme-toggler"),
					"topRight"
				);
				$("#nav-btn").click();
				return
			};
			$("#style-sheet").load(" #style-sheet");
			$("#theme-control").load(" #theme-toggler");
			$("#nav-btn").click();
			pushNotifications();
		}
	)
}

function wXs() {
	console.log("extra-small")
	$(".url--item").css("font-size", ".6rem");
	$(".url--item").css("padding", ".5rem")
}

function wSm() {
	console.log("small")
	$('.banner-img').css("height", "5cm")
	$(".url--item").css("font-size", ".6rem");
	$(".url--item").css("padding", ".68rem")
}

function wMd() {
	console.log("medium")
	$('.banner-img').css("height", "5.5cm");
	$("main").css("min-height", "15cm");
	$(".url--item").css("font-size", ".7rem");
	$(".url--item").css("padding", ".6rem")
}

function wLg() {
	console.log("large")
	$('.banner-img').css("height", "7cm")
	$(".url--item").css("font-size", "1.4rem");
	$(".url--item").css("padding", "1.2rem")
}

function wXl() {
	console.log("extra-large")
	$('.banner-img').css("height", "7.5cm")
	$(".url--item").css("font-size", "2rem");
	$(".url--item").css("padding", "1.5rem")
}

function viewPort(){
	var height = $(window).height();
	var width = $(window).width();
	if (height <= 575.98){
		// Extra small devices (portrait phones, less than 576px)
		wXs()
	} else if (height >= 576 && height <= 767.98) {
		// Small devices (landscape phones, 576px and up)
		wSm()
	} else if (height >= 768 && height <= 991.98) {
		// Medium devices (tablets, 768px and up)
		wMd()
	} else if (height >= 992 && height <= 1199.98) {
		// Large devices (desktops, 992px and up)
		wLg()			
	} else if (height >= 1200) {
		// Extra large devices (large desktops, 1200px and up)
		wXl()
	}
}

/*
create two css classes to handle filtering of search
1. input--menu{
	this is the menu object containing the input objects;
	this object contains a reference to an input called "iref"
	the value of iref should be a css selector of the referencing input;
}

2. input--menu-object{
	this are input objects that when selected would have a class called
	input--menu-selected{
		this class gives the element an :after checked-input
	};
	onclick{
		if this has an attr called "ivalue"{
			the value of ivalue would be supplied to the 
			parent(".input--menu") iref
		} else {
			the .text() is supplied to the 
			parent(".input--menu:first") iref
		}
        any siblings("input--menu-object") that was previously selected
        would be unselected
	}
}

*/

function handleFab(fab){
	if ($(fab).hasClass('fab')){
        $(fab).toggleClass('fab fab-active');
        $('.fab-info').addClass("fab-info-active")
	} else if ($(fab).hasClass('fab-active')){
		$(fab).toggleClass('fab fab-active');
		$('.fab-info').removeClass("fab-info-active")
	}
	$(fab).closest('div.floating-action-menu').toggleClass('active');
}

function getCurrentUrl(){
	$(".url--item").each(function(){
		if ($(this).attr("href") == document.location.pathname){
			$(this).addClass("active")
		}
	})
}

function applyCoupon(self){
	self = $(self)
	code = self.parent().children('input:not([type=hidden])')
	orderId = self.parent().children('input[type=hidden]')
	url = self.attr('url')
	// make sure container contains an .ajax-wrapper
	container = $(self.attr('container'))
	data = {
		code: code.val(),
		order_id: orderId.val()
	}
	request.post(url, data, function(data){
		toast(data.message, data.level, 2000)
		container.load(' #' + container.attr('id'))
	})
}



$(function(){
	main.setPrefferedMode();
	$(".input--menu-object").each(function(){
		if (!$(this).hasClass('fas')){
			$(this).addClass('fas')
		}
		$(this).bind("click", function(){
			parent = $(this).parent(".input--menu")
			iref = $(parent.attr("iref"))
			ivalue = $(this).attr("ivalue")
			if (ivalue == undefined){
				ivalue = $(this).text()
			}
			if ($(this).hasClass("input--menu-selected")){
			   $(this).removeClass("input--menu-selected")
			   iref.val("")
			} else {
				iref.val(ivalue)
				$(this).siblings(".input--menu-object").removeClass("input--menu-selected")
				$(this).addClass("input--menu-selected")
			}

		})
	});
	$('.clipboard-object').each(function(){
		var attr = $(this).attr('data-clipboard-text');
		if (isNone(attr)){
		  $(this).attr('data-clipboard-text', $(this).text())
		}
	})
	clipboard = new ClipboardJS('.clipboard-object')
	clipboard.on('success', function(e){
		msg = $(e.trigger).attr('data-clipboard-toast')
		if (!isNone(msg)){
			message(msg, "success")
		} else {
		    message("copied to clipboard", "success")
		}
	});
	clipboard.on('error', function(){
		message("could not copy to clipboard. try again", "error")
	})
	$("#not-mobile [data-toggle='tooltip']").tooltip()
	$(".fab").trigger("click");
    getCurrentUrl();
	$(window).on("resize", function(){/*location.reload(true); */viewPort()});
	pushNotifications();
	viewPort();
	$('img').each(function(){
		this.onerror = function(){$(this).replaceWith($(this).attr("alt") || "BROKEN IMAGE")};
	});


})

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
            $('#theme-fab').removeClass('fa-moon')
            $('#theme-fab').addClass('fa-sun')
        } else {
            $("#dm").remove();
            $("head:first").append($(this.lightmodeCss));
            this.createCookie("preferredTheme", "light-mode", 365);
            $('#theme-fab').removeClass('fa-sun')
            $('#theme-fab').addClass('fa-moon')
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
            $('#theme-fab').removeClass('fa-sun')
            $('#theme-fab').addClass('fa-moon')
        } else if (mode == 'light-mode'){
            $('#dm').remove()
            $("head:first").append($(this.lightmodeCss));
            $('#theme-fab').removeClass('fa-sun')
            $('#theme-fab').addClass('fa-moon')
        } else if (mode == 'dark-mode'){
            $('#lm').remove()
            $("head:first").append($(this.darkmodeCss));
            $('#theme-fab').removeClass('fa-moon')
            $('#theme-fab').addClass('fa-sun')
        }
    }
}
