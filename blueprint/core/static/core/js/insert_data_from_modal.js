function insert_data_from_modal(e, form_search, select_search, modal_search, drf_url) {
    let form = $(form_search);
    let select = $(select_search);
    let modal = $(modal_search);

    let formdata = new FormData(form[0]);

    $.ajax({
        url: drf_url,
        type: 'POST',
        data: formdata,
        processData: false,
        contentType: false,
        cache: false,
        success: function (data) {
            // Adicionando o item retornado no select
            select.load(window.location.href + " " + select_search + " option", function () {
                select.val(data.id);
            });

            modal.modal('hide');
            $("body").removeClass("modal-open");
            $(".modal-backdrop").remove();

            form.trigger("reset");
        },
        error: function (error) {
            let inputs = form.find("input, select, textarea");
            inputs.removeClass("is-invalid");
            inputs.siblings(".invalid-feedback").text("");

            let errors = error.responseJSON;
            for (let key in errors) {
                let field = form.find(`[name=${key}]`);
                field.addClass("is-invalid");
                field.siblings(".invalid-feedback").text(errors[key]);
            }
            modal.animate({
                scrollTop: 0
            }, "slow");
        }
    })
}