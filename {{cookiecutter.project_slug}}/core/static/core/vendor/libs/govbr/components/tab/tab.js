/** Classe para instanciar um objeto BRTab*/

class BRTab {
  /**
   * Instancia do objeto
   * @param {string} name - Nome do componente em minúsculo
   * @param {object} component - Objeto referenciando a raiz do componente DOM
   */
  constructor(name, component) {
    this.name = name
    this.component = component
    this._setBehavior()
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehavior() {
    for (const ancor of this.component.querySelectorAll('.tab-nav')) {
      this.height = ancor.clientHeight
      this.scollsizes = ancor.scrollHeight - ancor.clientHeight

      this.scrollHeight = Math.max(
        this.component.scrollWidth,
        document.documentElement.scrollWidth,
        this.component.offsetWidth,
        document.documentElement.offsetWidth,
        this.component.clientWidth,
        document.documentElement.clientWidth
      )
      this.leftPosition = this.component.offsetWidth - 1
      // debugger
      ancor.style.setProperty('--height-nav', `${this.height}px`)
      ancor.style.setProperty('--right-gradient-nav', `${this.leftPosition}px`)

      this.positionScroll(ancor)

      this.navigationRight = this.navigationRight + 4

      if (this.navigationRight <= this.lastItempos - 5) {
        ancor.classList.add('tab-nav-right')
      }

      ancor.onscroll = () => {
        this.positionScroll(ancor)

        if (this.navigationLeft <= 0) {
          ancor.classList.add('tab-nav-left')
        } else {
          ancor.classList.remove('tab-nav-left')
        }

        if (this.navigationRight <= this.lastItempos - 5) {
          ancor.classList.add('tab-nav-right')
        } else {
          ancor.classList.remove('tab-nav-right')
        }
      }
    }

    for (const ancor of this.component.querySelectorAll(
      '.tab-nav .tab-item:not([not-tab="true"]) button'
    )) {
      ancor.addEventListener(
        'click',
        (event) => {
          this._switchTab(event.currentTarget.parentElement)
          this._switchContent(event.currentTarget.parentElement)
        },
        false
      )
      ancor.addEventListener('keyup', (e) => {
        e.preventDefault()
        this.positionKeyboard(e)
      })

      ancor.addEventListener('blur', () => {
        this.hiddenTooltips()
      })
    }
    this.tabitems = this.component.querySelectorAll('tab-item')
  }

  /**
   * Mapeia as teclas pressionadas
   * @param {event} event - evento que disparou a ação
   */
  positionKeyboard(event) {
    const keys = {
      end: 35,
      home: 36,
      left: 37,
      right: 39,
      space: 32,
      tab: 9,
    }
    const key = event.keyCode
    this.tabitems = this.component.querySelectorAll('.tab-item')
    this.buttons = this.component.querySelectorAll('button')

    switch (key) {
      case keys.end:
        event.preventDefault()
        this.clean()
        this._switchTab(this.tabitems[this.tabitems.length - 1])
        this._switchContent(this.tabitems[this.tabitems.length - 1])
        this.tabitems[this.tabitems.length - 1].focus()
        break
      case keys.home:
        event.preventDefault()
        this.clean()
        this._switchTab(this.tabitems[0])
        this._switchContent(this.tabitems[0])
        this.tabitems[0].focus()
        event.stopPropagation()
        break
      case keys.left:
        event.preventDefault()
        this.position(event.target, -1)
        event.stopPropagation()
        break
      case keys.right:
        event.preventDefault()
        this.position(event.target, 1)
        event.stopPropagation()
        break
      case keys.tab:
        event.preventDefault()
        this.position(event.target, 0)
        event.stopPropagation()
        break
      case 32:
        event.preventDefault()
        this.hiddenTooltips()
        event.target.click()

        event.stopPropagation()
        break
      default:
        break
    }
  }

  /**
   *  Esconde todos tooltip
   *
   */
  hiddenTooltips() {
    const tooltips = document.querySelectorAll('.br-tooltip')

    tooltips.forEach((element) => {
      element.hidden = true
      element.style.visbility = 'hidden'
      element.removeAttribute('data-show')
    })
  }

  /**
   * Define o deslocamento da posição ativa
   * @property {object} target - referencia ao objeto DOM
   * @property {number} direction - incremento à posição
   */
  positionActive(target, direction) {
    let contComponent = 0
    let contComponentActive = 0

    const tabItems2 =
      target.parentElement.parentElement.querySelectorAll('.tab-item')
    for (const component of tabItems2) {
      if (
        component.classList.contains('is-active') ||
        component.classList.contains('active')
      ) {
        contComponentActive = contComponent
      }
      contComponent += 1
    }
    if (
      tabItems2.length > contComponentActive + direction &&
      contComponentActive + direction >= 0
    ) {
      this._switchTab(tabItems2[contComponentActive + direction])
      tabItems2[contComponentActive + direction].focus()
      let x = ''
      if (tabItems2[contComponentActive + direction].querySelector('button')) {
        x = tabItems2[contComponentActive + direction].querySelector('button')
        x.focus()
      }
    }
  }

  /**
   * Define o deslocamento da posição ativa do tab-item interno
   * @property {object} target - referencia ao objeto DOM
   * @property {number} direction - incremento à posição
   */
  position(target, direction) {
    this.positionQuery(target, direction, '.tab-item')
  }

  /**
   * Define o deslocamento da posição ativa do elemento referenciado
   * @property {object} target - referencia ao objeto DOM
   * @property {number} direction - incremento à posição
   * @property {string} query - string de referencia
   */
  positionQuery(target, direction, query) {
    let contComponent = 0
    // const contComponentActive = 0
    let contComponentFocus = 0
    const tabItems2 = target.parentElement.parentElement.querySelectorAll(query)
    for (const component of tabItems2) {
      if (component.querySelector('.focus-visible')) {
        contComponentFocus = contComponent
      }
      contComponent += 1
    }
    tabItems2[contComponentFocus + direction].querySelector('button').focus()
    if (
      tabItems2.length > contComponentFocus + direction &&
      contComponentFocus + direction >= 0
    ) {
      if (tabItems2[contComponentFocus + direction].querySelector('button')) {
        tabItems2[contComponentFocus + direction]
          .querySelector('button')
          .focus()
      }
    }
  }

  /**
   * Define a posição ativa do elemento referenciado
   * @property {object} target - referencia ao objeto DOM
   */
  setPosition(target) {
    let contComponent = 0
    let contComponentActive = 0

    const tabItems2 =
      target.parentElement.parentElement.querySelectorAll('.tab-item')
    for (const component of tabItems2) {
      if (
        component.classList.contains('is-active') ||
        component.classList.contains('active')
      ) {
        contComponentActive = contComponent
      }
      contComponent += 1
    }
    if (tabItems2.length > contComponentActive && contComponentActive >= 0) {
      this.clean()
      this._switchContent(tabItems2[contComponentActive])
    }
  }

  /**
   * Reinicia estados
   */
  clean() {
    for (const ancor of event.currentTarget.parentElement.querySelectorAll(
      'button'
    )) {
      ancor.classList.remove('focus-visible')
      ancor.classList.remove('is-active')
      ancor.classList.remove('active')
    }
    for (const ancor of event.currentTarget.parentElement.querySelectorAll(
      'tab-item'
    )) {
      ancor.classList.remove('is-active')
      ancor.classList.remove('active')
    }
  }

  /**
   * Realiza rolagem até a âncora
   * @property {object} ancor - referencia ao objeto DOM
   */
  positionScroll(ancor) {
    this.navItems = ancor.querySelectorAll('.tab-item')
    this.lastItempos = Math.ceil(
      this.navItems[this.navItems.length - 1].getBoundingClientRect().right
    )
    this.navigationLeft = Math.floor(
      this.navItems[0].getBoundingClientRect().left
    )
    this.navigationRight = Math.floor(ancor.getBoundingClientRect().right)
  }

  /**
   * Muda para a aba referenciada
   * @property {object} currentTab - referencia ao objeto DOM
   */
  _switchTab(currentTab) {
    for (const tabItem of this.component.querySelectorAll(
      '.tab-nav .tab-item:not([not-tab="true"])'
    )) {
      if (tabItem === currentTab) {
        tabItem.classList.add('active')
      } else {
        tabItem.classList.remove('is-active')
        tabItem.classList.remove('active')
      }
    }
  }

  /**
   * Muda para o conteudo da aba referenciada
   * @property {object} currentTab - referencia ao objeto DOM
   */
  _switchContent(currentTab) {
    for (const button of currentTab.querySelectorAll('button')) {
      for (const tabPanel of this.component.querySelectorAll(
        '.tab-content .tab-panel'
      )) {
        if (
          button.getAttribute('data-panel') === tabPanel.getAttribute('id') ||
          button.getAttribute('data-target') === tabPanel.getAttribute('id')
        ) {
          tabPanel.classList.add('active')
        } else {
          tabPanel.classList.remove('is-active')
          tabPanel.classList.remove('active')
        }
      }
    }
  }
}

export default BRTab
