/** Classe para instanciar um objeto BRMenu*/
class BRMenu {
	/**
	 * Instancia do objeto
	 * @param {string} name - Nome do componente em minúsculo
	 * @param {object} component - Objeto referenciando a raiz do componente DOM
	 */
	constructor(name, component) {
		this.name = name
		this.component = component
		this.id = this.component.id
		this.breakpoints = this.component.dataset.breakpoints
			? this.component.dataset.breakpoints.split(' ')
			: ['col-sm-4', 'col-lg-3']
		this.pushShadow = 'shadow-lg-right'
		this.trigger = document.querySelector(`[data-target="#${this.id}"]`)
		this.contextual = this.component.querySelector(
			'[data-toggle="contextual"]'
		)
		this.dismiss = this.component.querySelectorAll('[data-dismiss="menu"]')
		this.scrim = this.component.querySelector('.menu-scrim')
		this.componentFolders = this.component.querySelectorAll('.menu-folder')
		this.componentItems = this.component.querySelectorAll('.menu-item')
		this._setBehavior()
	}

	/**
	 * Define comportamentos do componente
	 * @private
	 */
	_setBehavior() {
		this._toggleMenu()
		this._setDropMenu()
		this._setSideMenu()
		this._setKeyboardBehaviors()
		this._setBreakpoints()
		this._setView()
		window.addEventListener('resize', () => {
			this._setView()
		})
	}

	/**
	 * Define visual do componente
	 * @private
	 */
	_setView() {
		const template = document.querySelector('body')
		const menuContextual = document.querySelector('.menu-trigger')
		// const panel = document.querySelector('.menu-panel')
		if (menuContextual && window.innerWidth < 992) {
			template.classList.add('mb-5')
		} else {
			template.classList.remove('mb-5')
		}
	}

	/**
	 * Define breakpoints do menu
	 * @private
	 */
	_setBreakpoints() {
		if (!this.component.classList.contains('push') && !this.contextual) {
			this.component
				.querySelector('.menu-panel')
				.classList.add(...this.breakpoints)
		}
	}

	/**
	 * Define ações do teclado
	 * @private
	 */
	_setKeyboardBehaviors() {
		// Fechar com tecla ESC
		this.component.addEventListener('keyup', (event) => {
			switch (event.code) {
				case 'Escape':
					this._closeMenu()
				default:
					break
			}
		})
		// Fechar com Tab fora do menu
		if (this.scrim) {
			this.scrim.addEventListener('keyup', () => {
				return this._closeMenu()
			})
		}
	}

	/**
	 * Define comportamentos de abrir/fechar menu
	 * @private
	 */
	_toggleMenu() {
		const trigger = this.contextual ? this.contextual : this.trigger
		// Clicar no trigger
		if (trigger) {
			trigger.addEventListener('click', () => {
				// Fechar Menu caso esteja aberto
				if (this.component.classList.contains('active')) {
					this._closeMenu()
					return
				}
				// Abre Menu
				this._openMenu()
				this._focusNextElement()
			})
		}
		// Clicar no dismiss
		for (const close of this.dismiss) {
			close.addEventListener('click', () => {
				return this._closeMenu()
			})
		}
	}

	/**
	 * Define visual do menu aberto
	 * @private
	 */
	_openMenu() {
		this.component.classList.add('active')
		if (this.component.classList.contains('push')) {
			this.component.classList.add(...this.breakpoints, 'px-0')
		}
		this.component.focus()
	}

	/**
	 * Define visual do menu fechado
	 * @private
	 */
	_closeMenu() {
		this.component.classList.remove('active')
		if (this.component.classList.contains('push')) {
			this.component.classList.remove(...this.breakpoints, 'px-0')
		}
		this._focusNextElement()
	}

	/**
	 * Configura Drop Menu para filho imediato de ".menu-folder"
	 * @private
	 */
	_setDropMenu() {
		for (const item of this.component.querySelectorAll(
			'.menu-folder > a.menu-item'
		)) {
			// Inclui ícone de Drop Menu
			this._createIcon(item, 'fa-chevron-down')
			// Configura como Drop Menu
			item.parentNode.classList.add('drop-menu')
			// Inicializa Drop Menu
			this._toggleDropMenu(item)
		}
	}

	/**
	 * Foca no próximo elemento
	 * @private
	 */
	_focusNextElement() {
		//lista de elementos que desejamos focar
		const focussableElements =
			'a:not([disabled]), button:not([disabled]), input[type=text]:not([disabled]), [tabindex]:not([disabled]):not([tabindex="-1"])'
		if (document.activeElement) {
			const focussable = Array.prototype.filter.call(
				document.body.querySelectorAll(focussableElements),
				(element) => {
					// testa a visibilidade e inclui o elemento ativo
					return (
						element.offsetWidth > 0 ||
						element.offsetHeight > 0 ||
						element === document.activeElement
					)
				}
			)
			const index = focussable.indexOf(document.activeElement)
			if (index > -1) {
				const nextElement = focussable[index + 1] || focussable[0]
				nextElement.focus()
			}
		}
	}

	/**
	 * Configura Side Menu para quem não for filho imediato de ".menu-folder"
	 * @private
	 */
	_setSideMenu() {
		for (const ul of this.component.querySelectorAll('a.menu-item + ul')) {
			if (!ul.parentNode.classList.contains('menu-folder')) {
				// Inclui ícone de Side Menu
				this._createIcon(ul.previousElementSibling, 'fa-angle-right')
				// Configura como Side Menu
				ul.parentNode.classList.add('side-menu')
				// Inicializa Side Menu
				this._toggleSideMenu(ul.previousElementSibling)
			}
		}
	}

	/**
	 * Muda estado do Drop Menu - aberto/fechado
	 * @private
	 * @param {object} element - referência ao Objeto que fará a ação
	 */
	_toggleDropMenu(element) {
		// Verifica se o elemento já possui click listener através de um atributo especial
		if (!element.hasAttribute('data-click-listener')) {
			element.addEventListener('click', () => {
				// Fecha Drop Menu caso esteja aberto
				if (element.parentNode.classList.contains('active')) {
					element.parentNode.classList.remove('active')
					return
				}

				// Abre Drop Menu
				element.parentNode.classList.add('active')
			})
			// Adiciona atributo especial para indicar que o elemento já possui click listener
			element.setAttribute('data-click-listener', 'true')
		}
	}

	/**
	 * Muda estado do Side Menu - aberto/fechado
	 * @private
	 * @param {object} element - referência ao Objeto que fará a ação
	 */
	_toggleSideMenu(element) {
		// Verifica se o elemento já possui click listener através de um atributo especial
		if (!element.hasAttribute('data-click-listener')) {
			element.addEventListener('click', () => {
				// Esconde todos os itens
				this._hideItems(element)

				// Mostra itens do Side Menu ativo
				this._showItems(element.parentNode)

				// Fecha Side Menu caso esteja aberto
				if (element.parentNode.classList.contains('active')) {
					this._closeSideMenu(element)
					element.focus()
					return
				}

				// Abre Side Menu
				element.parentNode.classList.add('active')
				element.focus()
			})
			// Adiciona atributo especial para indicar que o elemento já possui click listener
			element.setAttribute('data-click-listener', 'true')
		}
	}

	/**
	 * Fecha Side Menu
	 * @private
	 * @param {object} element - referência ao Objeto que fará a ação
	 */
	_closeSideMenu(element) {
		element.parentNode.classList.remove('active')
		// Verifica se existe Side Menu anterior, caso contrário mostra todos os itens de volta
		const parentFolder = element.parentNode.closest('.side-menu.active')
			? element.parentNode.closest('.side-menu.active')
			: element.closest('.menu-body')
		this._showItems(parentFolder)
	}

	/**
	 * Esconde os elementos proximos a referencia
	 * @private
	 * @param {object} element - referencia ao Objeto que fará a ação
	 */
	_hideItems(element) {
		for (const item of element
			.closest('.menu-body')
			.querySelectorAll('.menu-item')) {
			item.setAttribute('hidden', '')
		}
	}

	/**
	 * Mostra os elementos proximos a referencia
	 * @private
	 * @param {object} element - referência ao Objeto que fará a ação
	 */
	_showItems(element) {
		for (const item of element.querySelectorAll('.menu-item')) {
			item.removeAttribute('hidden')
		}
	}

	/**
	 * Cria icone filho a referencia
	 * @private
	 * @param {object} element - referência ao Objeto pai
	 * @param {string} icon - nome da classe font awesome do ícone
	 */
	_createIcon(element, icon) {
		// Verifica se já existe container para o ícone
		if (!element.querySelectorAll('span.support').length) {
			const menuIconContainer = document.createElement('span')
			menuIconContainer.classList.add('support')

			const menuIcon = document.createElement('i')
			menuIcon.classList.add('fas')
			menuIcon.classList.add(icon)
			menuIcon.setAttribute('aria-hidden', 'true')

			menuIconContainer.appendChild(menuIcon)
			element.appendChild(menuIconContainer)
		}
	}
}

export default BRMenu
