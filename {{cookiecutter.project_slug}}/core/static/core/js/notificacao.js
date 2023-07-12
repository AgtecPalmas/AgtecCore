$(document).ready(function () {
	document
		.querySelectorAll('[role="alert"].br-message')
		.forEach(function (element) {
			setTimeout(function () {
				element.remove();
			}, 5000);
		});
});
