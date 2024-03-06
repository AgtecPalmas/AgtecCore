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
    this.contextual = this.component.querySelector('[data-toggle="contextual"]')
    this.dismiss = this.component.querySelectorAll('[data-dismiss="menu"]')
    this.scrim = this.component.querySelector('.menu-scrim')
    this.componentFolders = this.component.querySelectorAll('.menu-folder')
    this.componentSiders = this.component.querySelectorAll('.side-menu')
    this.componentItems = this.component.querySelectorAll('.menu-item')
    this.elementOpenMenu = HTMLElement
    this.inSubmenu = false
    this.triggerParent = HTMLElement
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
    this._addARIAAttributes()
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
    this.component.addEventListener('keydown', (event) => {
      // Código da tecla

      const keyCode = event.code
      switch (keyCode) {
        case 'Escape':
          event.preventDefault()

          if (this.trigger) {
            this._closeMenu()
          }

          break
        case 'ArrowDown':
          event.preventDefault()
          this._navigateToNextElment(event.target, 1)
          break
        case 'ArrowUp':
          event.preventDefault()
          this._navigateToNextElment(event.target, -1)
          break
        default:
          break
      }
    })
    // Fechar com Tab fora do menu
    if (this.scrim) {
      // this.scrim.addEventListener('keyup', () => {
      //   return this._closeMenu()
      // })
    }
  }

  /**
   * Navega para o próximo elemento na lista com base em um operador.
   *
   * @param {HTMLElement} element - O elemento de referência a partir do qual a navegação será realizada.
   * @param {number} operator - Um operador numérico que indica a direção da navegação.
   *                             Um valor positivo indica a navegação para baixo, enquanto um valor negativo
   *                             indica a navegação para cima.
   */
  _navigateToNextElment(element, operator) {
    // Obtém o contêiner pai com base na hierarquia
    const parentFolder = element.parentNode.closest('.side-menu.active')
      ? element.parentNode.closest('.side-menu.active')
      : element.closest('.br-menu')
    // Obtém todos os elementos irmãos relacionados ao elemento de referência dentro do contêiner pai
    const elementSiblings =
      parentFolder.classList.contains('br-menu') ||
      parentFolder.classList.contains('menu-body')
        ? parentFolder.querySelectorAll(
            '.menu-body > .menu-item, .menu-body > .menu-folder > .menu-item,.menu-body > .menu-folder.active > .side-menu.active, .menu-body > .menu-folder.active > ul > li > .menu-item'
          )
        : parentFolder.querySelectorAll(
            '.side-menu.active > .menu-item,.side-menu.active > ul > li > .menu-item'
          )
    // Determina a posição do elemento de referência na lista de elementos irmãos
    const posicao = Array.from(elementSiblings).findIndex((el) => {
      return el === element
    })

    // Calcula a nova posição na lista com base no operador
    const soma = posicao + operator

    // Foca no próximo elemento na lista, ajustando para o início ou o final da lista se necessário
    if (soma >= 0 && soma < elementSiblings.length) {
      const nextElement = elementSiblings[soma]

      if (
        nextElement.getAttribute('role') === 'group' ||
        nextElement.getAttribute('role') === 'tree'
      ) {
        const nextSibling = elementSiblings[soma + operator]
        nextSibling.focus()
      } else {
        nextElement.focus()
      }
    } else {
      // Se a nova posição estiver fora dos limites, foca no primeiro ou no último elemento da lista, dependendo do operador
      const lastIndex = elementSiblings.length - 1
      const targetElement = operator === 1 ? 0 : lastIndex
      const target = elementSiblings[targetElement]
      target.focus()
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
      trigger.addEventListener('keydown', (event) => {
        if (event.code === 'Enter' || event.code === 'Space') {
          event.preventDefault() // Impede o comportamento padrão do botão Enter ou Space
          // Fechar Menu caso esteja aberto
          if (this.component.classList.contains('active')) {
            this._closeMenu()
          } else {
            // Abre Menu
            this._openMenu()

            this._focusOnFirstVisibleItem()
          }
        }
      })

      trigger.addEventListener('click', () => {
        // Fechar Menu caso esteja aberto
        if (this.component.classList.contains('active')) {
          this._closeMenu()
        } else {
          this._openMenu()
          this._focusOnFirstVisibleItem()
        }
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
   *  Focar no primeiro item de nível 1 visível
   * @private
   */
  _focusOnFirstVisibleItem() {
    const activeMenu = this.component.querySelector(
      '.menu-body .menu-item:not([hidden]):not(.inactive)'
    )
    if (activeMenu) {
      activeMenu.focus()
      activeMenu.scrollIntoView({ block: 'nearest' }) // Foca e traz para a visualização se necessário
      return
    }

    const firstVisibleItem = this.component.querySelector(
      '.menu-body > .menu-item:not([hidden]):not(.inactive)'
    )

    if (firstVisibleItem) {
      firstVisibleItem.focus()
      firstVisibleItem.scrollIntoView({ block: 'nearest' }) // Foca e traz para a visualização se necessário
    }
  }

  /**
   * Define visual do menu aberto
   * @private
   */
  _openMenu() {
    this.elementOpenMenu = document.activeElement
    this.component.classList.add('active')
    this.component.setAttribute('aria-expanded', 'true')
    this.elementOpenMenu.setAttribute('aria-expanded', 'true')

    if (this.component.classList.contains('push')) {
      this.component.classList.add(...this.breakpoints, 'px-0')
    }
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
    if (this.elementOpenMenu) {
      this.elementOpenMenu.setAttribute('aria-expanded', 'false')
    }
    this.elementOpenMenu.focus()
    // }
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
      //Configura aria indicando que submenu está fechado
      item.setAttribute('aria-expanded', 'false')
      // Inicializa Drop Menu
      this._handleMenuInteraction(item)
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
        this.component.querySelectorAll(focussableElements),
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
      const nextElement = focussable[index + 1] || focussable[0]
      nextElement.focus()
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
        ul.parentNode.setAttribute('role', 'none')
        // Inicializa Side Menu
        this._handleSideMenuInteraction(ul.previousElementSibling)
      }
    }
  }

  /**
   * Gerencia eventos de cliques e interações por teclado no menu - tecla espaço
   * @private
   * @param {object} element - referência ao Objeto que fará a ação
   */
  _handleMenuInteraction(element) {
    if (!element.hasAttribute('data-click-listener')) {
      element.addEventListener('click', () => {
        this._toggleDropMenu(element)
      })

      element.addEventListener('keydown', (event) => {
        const menuFolder = element.closest('.menu-folder')
        const menuItem = menuFolder.querySelector('a.menu-item')

        if (menuFolder) {
          if (event.key === ' ' || event.key === 'Spacebar') {
            if (menuItem && menuItem.classList.contains('focus-visible')) {
              event.preventDefault()
              this._toggleDropMenu(element)
            }
          }
          if (event.key === '2') {
            // event.preventDefault()

            this._toggleDropMenu(element)
          }
        }
      })

      element.setAttribute('data-click-listener', 'true')
    }
  }

  /**
   * Muda estado do Drop Menu - aberto/fechado
   * @private
   * @param {object} element - referência ao Objeto que fará a ação
   */
  _toggleDropMenu(element) {
    if (element.parentNode.classList.contains('active')) {
      // this.inSubmenu = false
      this._closeMenuElement(element)
    } else {
      element.parentNode.classList.add('active')
      element.setAttribute('aria-expanded', 'true')

      this.inSubmenu = true
      element.parentElement
        .querySelectorAll('ul li ul a')
        .forEach((menuItem) => {
          this.triggerParent = menuItem.parentElement
          menuItem.addEventListener('keydown', (event) => {
            const { parentElement } = menuItem.parentElement
            const keyCode = event.code

            switch (keyCode) {
              case 'Escape':
                event.preventDefault()
                this._backMenu(parentElement)
                break
              case 'Backspace':
                event.preventDefault()
                this._backMenu(parentElement)
                break
              case 'ArrowLeft':
                event.preventDefault()
                this._backMenu(parentElement)
                break
              default:
                break
            }
          })
        })
    }
  }

  _backMenu(parentElement) {
    //

    parentElement.parentElement.querySelector('[data-click-listener]').click()
  }

  _closeMenuElement(element) {
    element.parentNode.classList.remove('active')
    element.setAttribute('aria-expanded', 'false')
  }

  /**
   * Gerencia eventos de cliques e interações por teclado no Side Menu - tecla espaço
   * @private
   * @param {object} element - referência ao Objeto que fará a ação
   */
  _handleSideMenuInteraction(element) {
    // Verifica se o elemento já possui click listener através de um atributo especial
    if (!element.hasAttribute('data-click-listener')) {
      element.addEventListener('click', () => {
        this.inSubmenu = false
        this._toggleSideMenu(element)
      })

      element.addEventListener('keydown', (event) => {
        const sideMenu = element.closest('.side-menu')
        const menuItem = sideMenu.querySelector('a.menu-item')

        if (sideMenu) {
          if (event.key === ' ' || event.key === 'Spacebar') {
            if (menuItem && menuItem.classList.contains('focus-visible')) {
              event.preventDefault()
              this._toggleSideMenu(element)
            }
          }
        }
      })

      element.setAttribute('data-click-listener', 'true')
    }
  }

  /**
   * Muda estado do Side Menu - aberto/fechado
   * @private
   * @param {object} element - referência ao Objeto que fará a ação
   */
  _toggleSideMenu(element) {
    this._hideItems(element)

    // Mostra itens do Side Menu ativo
    element.setAttribute('aria-expanded', 'true')
    this._showItems(element.parentNode)

    // Fecha Side Menu caso esteja aberto
    if (element.parentNode.classList.contains('active')) {
      this._closeSideMenu(element)
      element.focus()
      return
    }

    // Abre Side Menu
    element.parentNode.classList.add('active')

    // Foca no primeiro item do Side Menu
    const submenu = element.nextElementSibling
    if (submenu) {
      const firstMenuItem = submenu.querySelector('.menu-item')
      if (firstMenuItem) {
        firstMenuItem.focus()
      }
    }
  }

  /**
   * Fecha Side Menu
   * @private
   * @param {object} element - referência ao Objeto que fará a ação
   */
  _closeSideMenu(element) {
    element.parentNode.classList.remove('active')
    element.setAttribute('aria-expanded', 'false')
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

  /**
   * Adiciona atributos role=menu e role=menuitem com base na hierarquia dos elementos
   * @private
   */
  _addARIAAttributes() {
    // Adiciona atributo role="menubar" à classe .menu-body
    const menuBody = this.component.querySelector('.menu-body')
    // menuBody.setAttribute('role', 'menubar')
    menuBody.setAttribute('role', 'tree')
    if (this.contextual) {
      menuBody.setAttribute('role', 'menubar')
    }

    // Adiciona atributo role="group" nos elementos .menu-item que são filhos de .menu-folder e não são drop-down
    const nonDropdownItems = this.component.querySelectorAll(
      '.menu-folder:not(.drop-menu) > .menu-item'
    )
    nonDropdownItems.forEach((item) => {
      item.setAttribute('role', 'tree')
      if (this.contextual) {
        item.setAttribute('role', 'menubar')
      }
    })

    // Adiciona atributo role="menuitem" somente aos elementos <a> com a classe .menu-item que não têm .menu-folder como pai
    const menuItems = this.component.querySelectorAll(
      '.menu-folder.drop-menu > a.menu-item, li > a.menu-item'
    )
    menuItems.forEach((item) => {
      item.setAttribute('role', 'treeitem')
      if (this.contextual) {
        item.setAttribute('role', 'menuitem')
      }
    })

    // Adiciona atributo role="menu" e aria-label nos elementos <ul> que são filhos de .side-menu
    const sideMenuLists = this.component.querySelectorAll('.side-menu > ul')
    sideMenuLists.forEach((list) => {
      const menuItem = list.parentNode.querySelector('.menu-item .content')
      const menuItemText = menuItem.textContent.trim()

      list.setAttribute('role', 'group')
      list.setAttribute('aria-label', menuItemText)
    })

    // Adiciona atributo role="menu" e aria-label nos elementos <ul> que são filhos de .menu-folder
    const menuFolderLists = this.component.querySelectorAll('.menu-folder > ul')
    menuFolderLists.forEach((list) => {
      const menuItem = list.parentNode.querySelector('.menu-item .content')
      const menuItemText = menuItem.textContent.trim()
      list.setAttribute('role', 'tree')
      if (this.contextual) {
        list.setAttribute('role', 'menubar')
      }
      list.setAttribute('aria-label', menuItemText)
    })

    const sideMenuItems = this.component.querySelectorAll(
      'li.side-menu > .menu-item'
    )
    for (const submenu of sideMenuItems) {
      submenu.setAttribute('aria-haspopup', 'true')
      submenu.setAttribute('aria-expanded', 'false')
    }

    const folderMenuItems = this.component.querySelectorAll(
      '.menu-folder.drop-menu > .menu-item'
    )
    for (const submenu of folderMenuItems) {
      submenu.setAttribute('aria-haspopup', 'true')
      submenu.setAttribute('aria-expanded', 'false')
    }
  }
}

export default BRMenu
