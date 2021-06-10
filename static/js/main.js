function toast(text, type, timeout, callback, position){
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

function isNone(obj){
	if ((typeof obj == typeof undefined || Boolean(obj) == false)){
	    return true
	} else {
		return false
	}
	
}

function message(text, type){
	toast(text, type, 4000, function(){}, "topRight")
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
	get: function(path, body, callback){
		body.ajax = 1
		$.get(path, body, callback)
	},
	post: function(path, body, callback){
		body.ajax = 1
		$.ajax({
			url: path,
			type: "POST",
			data: body,
			headers: {"X-CSRFToken": getCookie("csrftoken")},
			success: callback
		})
	}
}


function addToCart(self){
	$.ajax({
		"url" : $(self).attr('url')+ '?ajax=1',
		"type" : "GET",
		"success" : function(data) {
			$("#cart-count").load("/?ajax=1 #cart-counter")
			card = $(self).closest('.product-card')
			card.load(" #" + card.attr('id') + ' .ajax-wrapper', {"ajax": 1})
			toast(
				data.message,
				data.level,
				2000,
				null
			)
		}
	})
}

function addToWishlist(self){
	$.ajax({
		"url" : $(self).attr('url')+ '?ajax=1',
		"type" : "GET",
		"success" : function(data) {
			$("#wish-count").load("/?ajax=1 #wish-counter")
			card = $(self).closest('.product-card')
			card.load("?ajax=1 #" + card.attr('id') + ' .ajax-wrapper')
			toast(
				data.message,
				data.level,
				2000,
				null
			)
		}
	})
}

function darkMode(){
	request.post(
		"/theme",
		{"dm": 1},
		function(data){
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
			
			
		}
	)
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