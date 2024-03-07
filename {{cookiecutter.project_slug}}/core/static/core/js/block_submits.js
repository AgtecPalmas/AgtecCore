// Coleta todos os botões de submit e adiciona um evento de clique que desabilita o botão e adiciona um spinner
const submitButtons = document.querySelectorAll(
	'input[type="submit"], button[type="submit"]'
);

function escapeHtml(text) {
	const div = document.createElement('div');
	div.textContent = text;
	return div.innerHTML;
}

function disableSubmitButton(event) {
	const button = event.target;

	if (!button.closest("form").checkValidity()) {
		return;
	}

	submitButtons.forEach((button) => {
		button.closest("div").setAttribute("disabled", true);
	});

	button.setAttribute("aria-busy", true);

	const text = escapeHtml(button.value || button.innerText || button.textContent || "Enviando...");
	button.innerHTML =
		'<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span> ' +
		text;

}

submitButtons.forEach((button) => {
	button.addEventListener("click", disableSubmitButton);
});
