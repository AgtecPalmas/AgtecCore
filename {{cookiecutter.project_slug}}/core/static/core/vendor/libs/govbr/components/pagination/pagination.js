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
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehaviors() {
    this._setActive()
    this._dropdownBehavior()
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
        this.currentPage = parseInt(page.querySelector('a'))
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
      page.addEventListener('click', (event) => {
        this._selectPage(event.currentTarget)
      })
    }
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
    })
    currentPage.classList.add('active')
    this._setLayout()
  }
}

export default BRPagination
