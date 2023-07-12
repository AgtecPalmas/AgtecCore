import Tooltip from '../../partial/js/behavior/tooltip'

/** Classe para instanciar um objeto BRHeader*/
class BRHeader {
  /**
   * Instancia do objeto
   * @param {string} name - Nome do componente em minúsculo
   * @param {object} component - Objeto referenciando a raiz do componente DOM
   */
  constructor(name, component) {
    this.name = name
    this.component = component
    this.componentSearch = this.component.querySelector('.header-search')
    this.componentSearchInput = this.component.querySelector(
      '.header-search input'
    )
    this.componentSearchTrigger = this.component.querySelector(
      '[data-toggle="search"]'
    )
    this.componentSearchDismiss = this.component.querySelector(
      '[data-dismiss="search"]'
    )
    this.hideDrop = null
    this.menuTrigger = this.component.querySelector(
      '[data-target="#main-navigation"]'
    )
    this._setBehavior()
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehavior() {
    this._setLogoutBehavior()
    this._setSearchBehaviors()
    this._setKeyboardBehaviors()
    this._setDropdownBehavior()
    this._setSticky()
  }

  /**
   * Define comportamentos de login
   * @private
   */
  _setLoginBehavior() {
    for (const login of this.component.querySelectorAll(
      '[data-trigger="login"]'
    )) {
      login.addEventListener('click', () => {
        const loginParent = login.closest('.header-login')
        loginParent.querySelector('.header-sign-in').classList.add('d-none')
        loginParent.querySelector('.header-avatar').classList.remove('d-none')
      })
    }
  }

  /**
   * Define comportamentos de logout
   * @private
   */
  _setLogoutBehavior() {
    for (const logout of this.component.querySelectorAll(
      '[data-trigger="logout"]'
    )) {
      logout.addEventListener('click', () => {
        const logoutParent = logout.closest('.header-login')
        logoutParent.querySelector('.avatar').classList.remove('show')
        logoutParent
          .querySelector('[data-toggle="dropdown"]')
          .classList.remove('active')
        logoutParent.querySelector('.header-sign-in').classList.remove('d-none')
        logoutParent.querySelector('.header-avatar').classList.add('d-none')
      })
    }
  }

  /**
   * Define comportamentos de busca
   * @private
   */
  _setSearchBehaviors() {
    // Abrir busca
    if (this.componentSearchTrigger) {
      this.componentSearchTrigger.addEventListener('focus', () => {
        this._cleanDropDownHeader()
      })
      this.componentSearchTrigger.addEventListener('click', () => {
        this._openSearch()
      })
    }

    // Fechar busca
    if (this.componentSearchDismiss) {
      this.componentSearchDismiss.addEventListener('click', () => {
        this._closeSearch()
      })
    }
  }

  /**
   * Define comportamentos do teclado
   * @private
   */
  _setKeyboardBehaviors() {
    if (this.componentSearchInput) {
      this.componentSearchInput.addEventListener('keydown', (event) => {
        switch (event.keyCode) {
          // Tecla ESC
          case 27:
            this._closeSearch()
            break
          default:
            break
        }
      })
    }
    for (const trigger of this.component.querySelectorAll(
      '.dropdown [data-toggle="dropdown"]'
    )) {
      trigger.addEventListener('keydown', (event) => {
        switch (event.keyCode) {
          // Tecla ESC
          case 32:
            if (event.target.parentNode.classList.contains('show')) {
              event.target.parentNode.click()
              event.target.parentNode.classList.remove('show')
              event.target.classList.remove('active')
              event.stopPropagation()
            }
            break
          default:
            break
        }
      })
    }
  }

  /**
   * Visualização da busca
   * @private
   */
  _openSearch() {
    if (this.componentSearch) {
      this.componentSearch.classList.add('active')
      this.componentSearch.querySelector('input').focus()
    }
  }

  /**
   * Esconde a busca
   * @private
   */
  _closeSearch() {
    if (this.componentSearch) {
      this.componentSearch.classList.remove('active')
      //this.componentSearchTrigger.focus()
      this._nextFocusElement().focus()
    }
  }

  /**
   * Exibe notificação
   * @param {event} event - referencia ao evento
   */
  handleEvent(event) {
    const hasNotficiationElemeent = this.component
      .querySelector('.br-notification')
      .contains(event.target)
    if (!hasNotficiationElemeent) {
      if (this.activateTr !== event.target.parentNode) {
        this._cleanDropDownHeaderRef(this.component)
      }
    }
  }

  /**
   * Define comportamentos do dropdown
   * @private
   */
  _setDropdownBehavior() {
    // TODO: Trocar o código abaixo pelo utilitário dropdown
    this.cleaned = false
    let hideDrop
    this.activateTr = 'teste'

    for (const trigger of this.component.querySelectorAll(
      '.dropdown [data-toggle="dropdown"]'
    )) {
      // eslint-disable-next-line no-loop-func
      trigger.addEventListener('click', (event) => {
        this._headerTooltip()
        clearTimeout(hideDrop)

        this.activateTr = trigger
        document.addEventListener('mousedown', this, false)
        event.stopImmediatePropagation()
        // Toggle de abrir / fechar
        const hasShow = trigger.classList.contains('active')

        if (hasShow) {
          trigger.classList.remove('active')
          trigger.closest('.dropdown').classList.remove('show')
        } else {
          this._cleanDropDownHeader()
          trigger.classList.add('active')
          trigger.closest('.dropdown').classList.add('show')

          // Evita que o componente feche o drop ao navegar pelo teclado
          const next = this._nextFocusElement()
          next.addEventListener('focus', () => {
            clearTimeout(hideDrop)
          })
        }
        event.stopPropagation()
        return ''
      })

      // Faz o drop fechar ao clicar fora
      // eslint-disable-next-line no-loop-func
    }
    this.menuTrigger.addEventListener('focus', () => {
      this._cleanDropDownHeader()
    })
  }

  /**
   * Define comportamentos do tooltip
   * @private
   */
  _headerTooltip() {
    if (this.TooltipExampleList) {
      this.TooltipExampleList.forEach((tooltipElem) => {
        tooltipElem.component.remove()
        tooltipElem.popperInstance.destroy()
      })
    }
    this.TooltipExampleList = []

    this.component
      .querySelectorAll('.notification-tooltip')
      .forEach((TooltipExample) => {
        const texttooltip = TooltipExample.getAttribute('data-tooltip-text')
        const config = {
          activator: TooltipExample,
          placement: 'top',
          textTooltip: texttooltip,
        }
        const x = new Tooltip(config)

        this.TooltipExampleList.push(x)
      })
  }

  /**
   * Limpa referencias do dorpdown
   * @private
   * @param {object} ref - Referência ao componente header
   */
  _cleanDropDownHeaderRef(ref) {
    if (this.cleaned === false) {
      for (const trigger of ref.querySelectorAll('.dropdown.show')) {
        trigger.classList.remove('show')
        trigger.parentNode.classList.remove('show')
        for (const button of ref.querySelectorAll('.br-button')) {
          button.classList.remove('active')
        }
      }
    }
    this.cleaned = false
  }

  /**
   * Limpa referencias do dorpdown
   * @private
   */
  _cleanDropDownHeader() {
    this._cleanDropDownHeaderRef(this.component)
  }

  /**
   * Define modo sticky ao header
   * @private
   */
  _setSticky() {
    if (this.component.hasAttribute('data-sticky')) {
      window.onscroll = () => {
        if (window.pageYOffset > this.component.offsetHeight) {
          this.component.classList.add('sticky', 'compact')
        } else {
          this.component.classList.remove('sticky', 'compact')
        }
      }
    }
  }

  /**
   * Foca no próximo elmento de ação
   * @private
   */
  _nextFocusElement() {
    //lista de elementos de ação
    const focussableElements =
      'a:not([disabled]), button:not([disabled]), input[type=text]:not([disabled]), [tabindex]:not([disabled]):not([tabindex="-1"])'
    if (document.activeElement) {
      const focussable = Array.prototype.filter.call(
        document.body.querySelectorAll(focussableElements),
        (element) => {
          //check for visibility while always include the current activeElement
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
        //nextElement.focus();
        return nextElement
      }
    }
    return null
  }
}

export default BRHeader
