// Coleta todos os botões de submit e adiciona um evento de clique que desabilita o botão e adiciona um spinner
const submitButtons = document.querySelectorAll(
	'input[type="submit"], button[type="submit"]'
);

function disableSubmitButton(event) {
	const button = event.target;
	button.closest(".card-footer").setAttribute("disabled", true);
	const text = button.value || button.innerText || button.textContent;
	button.innerHTML =
		'<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span> ' +
		text;
}

submitButtons.forEach((button) => {
	button.addEventListener("click", disableSubmitButton);
});
