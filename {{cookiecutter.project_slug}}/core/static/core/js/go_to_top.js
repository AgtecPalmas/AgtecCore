$(document).ready(function () {
	$(".go-to-top").hide();

	$(window).scroll(function () {
		if ($(this).scrollTop() > 200) {
			$(".go-to-top").fadeIn(200);
		} else {
			$(".go-to-top").fadeOut(200);
		}
	});

	$(".go-to-top").click(function (event) {
		event.preventDefault();
		$("html, body").animate({ scrollTop: 0 }, 300);
	});
});
