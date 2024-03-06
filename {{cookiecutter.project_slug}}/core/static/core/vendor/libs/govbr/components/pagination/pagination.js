/** Classe para instanciar um objeto BRPagination*/
class BRPagination {
  /**
   * Instancia do objeto
   * @param {string} name - Nome do componente em minúsculo
   * @param {object} component - Objeto referenciando a raiz do componente DOM
   */
  constructor(name, component) {
    this.name = name
    this.component = component
    this.currentPage = 1
    this._setBehaviors()
    this._adaptSelectAccessibility()
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehaviors() {
    this._setKeybordBehavior()
    this._setActive()
    this._dropdownBehavior()
  }

  /**
   * Define o comportamento de algumas teclas
   * @private
   */
  _setKeybordBehavior() {
    this._setDefaultPaginationKeybordBehavior()
    this._setContextualPaginationKeyboardBehavior()
  }

  _setDefaultPaginationKeybordBehavior() {
    this.component.querySelectorAll('li *:first-child').forEach((element) => {
      element.addEventListener('keydown', (event) => {
        if (
          event.key === 'ArrowLeft' &&
          !element.hasAttribute('data-previous-page')
        ) {
          element.parentElement.previousElementSibling.children[0].focus()
        }
        if (
          event.key === 'ArrowRight' &&
          !element.hasAttribute('data-next-page')
        ) {
          element.parentElement.nextElementSibling.children[0].focus()
        }
        if (
          event.key === 'ArrowDown' &&
          element.nextElementSibling?.classList.contains('br-list')
        ) {
          element.nextElementSibling.children[0].focus()
        }
      })
    })
  }

  _setContextualPaginationKeyboardBehavior() {
    this.component
      .querySelectorAll('.pagination-per-page .br-list')
      .forEach((element) => {
        element.addEventListener('keydown', (event) => {
          if (event.key === 'Escape') {
            event.currentTarget.parentElement.focus()
          }
        })
      })
  }

  /**
   * Define visual do componente
   * @private
   */
  // eslint-disable-next-line complexity
  _setLayout() {
    const ul = this.component.querySelector('ul')
    const pages = this.component.querySelectorAll('.page')
    pages.forEach((page) => {
      if (page.classList.contains('active')) {
        this.currentPage = parseInt(page.innerText)
      }
      page.classList.remove('d-none')
    })

    if (this.currentPage === 1) {
      ul.querySelector('[data-previous-page]').setAttribute('disabled', '')
    } else {
      ul.querySelector('[data-previous-page]').removeAttribute('disabled')
    }

    if (this.currentPage === pages.length) {
      ul.querySelector('[data-next-page').setAttribute('disabled', '')
    } else {
      ul.querySelector('[data-next-page]').removeAttribute('disabled')
    }

    if (pages.length > 9) {
      if (this.currentPage < 6) {
        if (ul.querySelector('[data-previous-interval]')) {
          ul.querySelector('[data-previous-interval]').remove()
        }
        for (let page = 7; page < pages.length - 1; page++) {
          pages[page].classList.add('d-none')
        }
        if (!ul.querySelector('[data-next-interval]')) {
          ul.insertBefore(
            this._createIntervalElement('next'),
            ul.children[ul.children.length - 2]
          )
        }
      }
      if (this.currentPage >= 6 && this.currentPage < pages.length - 4) {
        for (let page = this.currentPage - 4; page > 0; page--) {
          pages[page].classList.add('d-none')
        }
        if (!ul.querySelector('[data-previous-interval]')) {
          ul.insertBefore(
            this._createIntervalElement('previous'),
            ul.children[2]
          )
        }
        for (let page = this.currentPage + 2; page < pages.length - 1; page++) {
          pages[page].classList.add('d-none')
        }
        if (!ul.querySelector('[data-next-interval]')) {
          ul.insertBefore(
            this._createIntervalElement('next'),
            ul.children[ul.children.length - 2]
          )
        }
      }
      if (this.currentPage >= pages.length - 4) {
        if (ul.querySelector('[data-next-interval]')) {
          ul.querySelector('[data-next-interval]').remove()
        }
        for (let page = pages.length - 8; page > 0; page--) {
          pages[page].classList.add('d-none')
        }
        if (!ul.querySelector('[data-previous-interval]')) {
          ul.insertBefore(
            this._createIntervalElement('previous'),
            ul.children[2]
          )
        }
      }
    }
  }

  /**
   * Cria elemento no intervalo
   * @param {string} type - nome do tipo do elmento
   * @private
   */
  _createIntervalElement(type) {
    const interval = document.createElement('li')
    interval.setAttribute(`data-${type}-interval`, '')

    const a = document.createElement('a')
    a.setAttribute('href', 'javascript:void(0)')

    const icon = document.createElement('i')
    icon.classList.add('fas', 'fa-ellipsis-h')

    a.appendChild(icon)
    interval.appendChild(a)

    return interval
  }

  /**
   * Cria ação de clique na página
   * @private
   */
  _setActive() {
    for (const page of this.component.querySelectorAll('.page')) {
      if (this.currentPage === Number(page.innerText)) {
        page.setAttribute('aria-current', 'page')
      } else {
        page.removeAttribute('aria-current')
      }

      page.addEventListener('click', (event) => {
        this._selectPage(event.currentTarget)
      })
    }
    // debugger
    for (const page of this.component.querySelectorAll(
      '.pagination-ellipsis .br-item'
    )) {
      page.addEventListener('click', (event) => {
        this._selectPage(event.currentTarget)
      })
    }
  }

  _initializeDropdownItems() {
    this.component.querySelectorAll('.br-list').forEach((list) => {
      const dropdownItems = Array.from(list.querySelectorAll('.br-item'))

      dropdownItems.forEach((item) => {
        item.addEventListener('keydown', (event) => {
          const { key } = event
          const currentIndex = dropdownItems.indexOf(item)
          const lastIndex = dropdownItems.length - 1

          switch (key) {
            case 'ArrowUp':
              event.preventDefault()
              const prevIndex =
                (currentIndex - 1 + dropdownItems.length) % dropdownItems.length
              dropdownItems[prevIndex].focus()
              break
            case 'ArrowDown':
              event.preventDefault()
              const nextIndex = (currentIndex + 1) % dropdownItems.length
              dropdownItems[nextIndex].focus()
              break
            default:
              break
          }
        })
      })
    })
  }

  /**
   * Cria comportamentos do dropdown
   * @private
   */
  _dropdownBehavior() {
    for (const dropdown of this.component.querySelectorAll(
      '[data-toggle="dropdown"]'
    )) {
      this._dropdownInit(dropdown)
      this._dropdownToggle(dropdown)
    }
  }

  /**
   * Cria ação de clique no dropdown
   * @param {object} element - referencia ao objeto DOM
   * @private
   */
  _dropdownToggle(element) {
    element.addEventListener('click', () => {
      if (element.getAttribute('aria-expanded') === 'false') {
        this._dropdownOpen(element)
        return
      }
      this._dropdownClose(element)
    })

    window.document.addEventListener('click', (event) => {
      if (!this.component.contains(event.target)) {
        this._dropdownClose(element)
      }
    })

    /**
     * Adiciona um ouvinte de eventos ao documento para capturar a tecla "Esc" pressionada.
     *
     * @param {HTMLElement} element - O elemento associado ao dropdown que deve ser fechado.
     */
    element.nextElementSibling.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        this._dropdownClose(element)
        const buttonInsideLi = element.parentElement.querySelector('button')
        if (buttonInsideLi) {
          buttonInsideLi.focus()
        }
      }
      if (event.key === 'Tab') {
        const items = event.currentTarget.querySelectorAll('.br-item')
        if (items[items.length - 1].hasAttribute('data-focus-visible-added')) {
          this._dropdownClose(element)
        }
      }
    })
  }

  /**
   * Inicializa elemento de dropdown
   * @param {object} element - referencia ao objeto DOM
   * @private
   */
  _dropdownInit(element) {
    element.parentElement.classList.add('dropdown')
    element.nextElementSibling.setAttribute('role', 'menu')
    element.setAttribute('aria-haspopup', 'true')
    this._dropdownClose(element)
    this._initializeDropdownItems()
  }

  /**
   * Ação de abrir dropdown
   * @param {object} element - referencia ao objeto DOM
   * @private
   */
  _dropdownOpen(element) {
    element.setAttribute('aria-expanded', 'true')
    element.nextElementSibling.removeAttribute('hidden')
  }

  /**
   * Ação de fechar dropdown
   * @param {object} element - referencia ao objeto DOM
   * @private
   */
  _dropdownClose(element) {
    element.setAttribute('aria-expanded', 'false')
    element.nextElementSibling.setAttribute('hidden', '')
  }

  /**
   * Define página ativa
   * @param {object} currentPage - referencia ao objeto DOM
   * @private
   */
  _selectPage(currentPage) {
    this.component.querySelectorAll('.page').forEach((page) => {
      page.classList.remove('active')
      page.removeAttribute('aria-current')
    })
    this.component.querySelectorAll('.br-item').forEach((page) => {
      page.classList.remove('active')
      page.removeAttribute('aria-current')
    })

    currentPage.classList.add('active')
    currentPage.setAttribute('aria-current', 'page')

    this._setLayout()
  }

  _adaptSelectAccessibility() {
    window.addEventListener('load', () => {
      this.component
        .querySelectorAll('.pagination-per-page .br-select .br-list')
        .forEach((element) => {
          element.setAttribute('role', 'menu')
          element.querySelectorAll('.br-item').forEach((item) => {
            item.setAttribute('role', 'menuitem')
          })
        })
    })
  }
}

export default BRPagination
