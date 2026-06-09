$(document).ready(function () {
	const warning = $(
		'<div id="development-warning"\
            class="rounder-md fw-bold p-3 bg-danger text-white"\
            style="position: fixed; bottom: 0; right: 0; z-index: 9999;">\
            SITE EM DESENVOLVIMENTO\
        </div>'
	);
	$("body").append(warning);
});
