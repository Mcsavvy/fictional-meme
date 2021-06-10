$(function() {
    $(".control").click(function() {
		$(".form-signin").toggleClass("form-signin-left");
		$(".form-signup").toggleClass("form-signup-left");
		$(".frame").toggleClass("frame-long");
		$(".signup-inactive").toggleClass("signup-active");
		$(".signin-active").toggleClass("signin-inactive");
		$(".forgot").toggleClass("forgot-left");
		$(this).removeClass("idle").addClass("active");
		$(".control").removeClass("xhide");
		$(this).addClass("xhide");
    });
});

$(".form-signup input[name='username']").on('change', function(e){
	if ($(this).val().length > 1){
		request(
			"GET",
			"/api/user/exists/" + $(this).val(),
			{},
			function(data) {
				if (data != null){
					toast(
						data.message,
						data.level,
						2000,
						$(
							".form-signup input[name='username']"
						).val(data.suggested),
						"topRight"
					)
				}
			}
		)
	}
})
