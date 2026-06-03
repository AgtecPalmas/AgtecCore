
$(document).ready(function () {
    let url = new URL(window.location.href);

    let sort_by = url.searchParams.get("sort_by");
    if (sort_by !== null) {
        $('#sort_by').val(sort_by);
    }

    let order_by = url.searchParams.get("order_by");
    if (order_by === 'asc') {
        $('#asc_order').addClass('active');

    } else {
        $('#desc_order').addClass('active');
    }
});

$('#form_order').submit(function (e) {
    e.preventDefault();

    let url = new URL(window.location.href);

    url.searchParams.set('sort_by', $('#sort_by').val());
    url.searchParams.set('order_by', e.originalEvent.submitter.value);

    window.location.href = url;
});