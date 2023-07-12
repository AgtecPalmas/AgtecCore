import Checkgroup from '../../partial/js/behavior/checkgroup'
import { CookiebarData } from './cookiebar-data'
import { CookiebarTemplates } from './cookiebar-templates'
import * as selectors from './selectors'

/** Classe para instanciar um objeto cookiebar */
export default class BRCookiebar {
  /**
   * Instancia um objeto cookiebar
   * @param {object} objeto - Objeto para destructuring com as propriedades abaixo
   * @property {string} name - Nome do componente em minúsculo (br-cookiebar)
   * @property {object} component - Objeto referenciando a raiz do componente DOM
   * @property {string} json - JSON de entrada com dados do cookiebar
   * @property {string} lang - Lingua para filtrar o JSON de entrada
   * @property {string} mode - Mode de renderização do cookibar ('default' | 'open')
   * @property {function} callback - Chamada no aceite do cookiebar com o JSON de saída como argumento
   */
  constructor({ name, component, json, lang, mode = 'default', callback }) {
    this.name = name
    this.component = component
    this.data = new CookiebarData(json, lang)
    this.templates = new CookiebarTemplates(this.data)
    this.mode = mode
    this.callback = callback
    this._setUp()
  }

  /**
   * Controla a instanciação do cookiebar
   * @private
   */
  _setUp() {
    this._buildCookiebar()
    this._setBehavior()
    this._showCookiebar()
  }

  /**
   * Controla a construção do cookiebar com o uso de templates
   * @private
   */
  _buildCookiebar() {
    this.component.innerHTML = this.templates.setGlobalContentArea()
  }

  /**
   * Controla o comportamento dos itens interativos do cookiebar
   * @private
   */
  _setBehavior() {
    this._setAcceptButtonBehavior()
    this._setPoliticsButtonBehavior()
    this._setCloseButtonBehavior()
    this._setToggleGroupBehavior()
    this._setCheckboxBehavior()
    this._setSelectionBehavior()
    this._setWindowResizeBehavior()
  }

  /**
   * Trata o comportamento do botão de aceite do cookiebar
   * @private
   */
  _setAcceptButtonBehavior() {
    const acceptButton = this.component.querySelector(selectors.ACCEPT_BUTTON)

    // Trata o aceite do cookiebar
    acceptButton.addEventListener('click', () => {
      this._hideCookiebar()
      // this._resetCookiebar()
      document.body.style.overflowY = 'auto'
      this.callback(this._setOutputJSON())
    })

    // (Navegação por teclado) Mantém o foco no cookiebar quando ele está aberto
    acceptButton.addEventListener('keydown', (event) => {
      if (event.key === 'Tab') {
        if (!this.component.classList.contains('default')) {
          this.component.focus()
        }
      }
    })

    this._setActionButtonResponsive(acceptButton)
  }

  /**
   * Trata o comportamento do botão de políticas/definições de cookies
   * @private
   */
  _setPoliticsButtonBehavior() {
    this.component
      .querySelectorAll(selectors.POLITICS_BUTTON)
      .forEach((politicsButton) => {
        // Expande o cookiebar
        politicsButton.addEventListener('click', () => {
          politicsButton.classList.add('d-none')
          this.component.classList.remove('default')
          this.component.focus()
          document.body.style.overflowY = 'hidden'
          this._setOpenView()
        })

        this._setActionButtonResponsive(politicsButton)
      })
  }

  /**
   * Trata o comportamento do botão de fechar do cookiebar no modo open
   * @orivate
   */
  _setCloseButtonBehavior() {
    this.component
      .querySelectorAll(selectors.CLOSE_BUTTON)
      .forEach((closeButton) => {
        // encolhe o cookiebar (volta ao cookiebar default)
        closeButton.addEventListener('click', () => {
          this.component.classList.add('default')
          switch (this.mode) {
            case 'open':
              this._hideCookiebar()
            // this._resetCookiebar()
            default:
          }

          this.component
            .querySelector(selectors.POLITICS_BUTTON)
            .classList.remove('d-none')
          document.body.style.overflowY = 'auto'

          this._setDefaultView()
        })
      })
  }

  /**
   * Trata o redimensionamento da tela
   * @private
   */
  _setWindowResizeBehavior() {
    window.addEventListener('resize', () => {
      if (!this.component.classList.contains('default')) {
        this._setOpenView()
      }
      this.component
        .querySelectorAll(selectors.ACTION_BUTTONS)
        .forEach((button) => {
          this._setActionButtonResponsive(button)
        })
    })
  }

  /**
   * Trata a responsividade de um botão de ação baseado na largura da tela
   * @param {object} button - Elemento DOM que representa um botão de ação
   * @private
   */
  _setActionButtonResponsive(button) {
    if (window.matchMedia('(max-width: 574px)').matches) {
      button.classList.add('block')
    }
    if (window.matchMedia('(min-width: 575px)').matches) {
      button.classList.remove('block')
    }
  }

  /**
   * Trata a abertura/fechamento do grupo de cookies
   * @private
   */
  _setToggleGroupBehavior() {
    this.component
      .querySelectorAll(
        `${`${selectors.GROUP_BUTTON}, ${selectors.GROUP_NAME}, ${selectors.COOKIES_CHECKED}, ${selectors.GROUP_SIZE}`}`
      )
      .forEach((clickable) => {
        clickable.addEventListener(
          'click',
          this._handleToggleGroupClick.bind(this)
        )
      })
  }

  /**
   * Handler que trata do evento de click no grupo
   * @param {object} event - Objeto Event
   * @private
   */
  _handleToggleGroupClick(event) {
    const element = this._getParentElementByClass(
      event.currentTarget,
      'br-item'
    )
    if (element.classList.contains('open')) {
      element.classList.remove('open')
      element.nextElementSibling
        .querySelectorAll(selectors.BR_SWITCH)
        .forEach((check) => {
          check.setAttribute('tabindex', -1)
        })
      this._setGroupAttributes(element, 'Expandir')
      this._toggleIcon(element, 'fa-angle-up', 'fa-angle-down')
    } else {
      element.classList.add('open')
      element.nextElementSibling
        .querySelectorAll(selectors.BR_SWITCH)
        .forEach((check) => {
          check.setAttribute('tabindex', 0)
        })
      this._setGroupAttributes(element, 'Retrair')
      this._toggleIcon(element, 'fa-angle-down', 'fa-angle-up')
      this._scrollUp(element)
    }
  }

  /**
   * Trata do comportamento do grupo de checkboxes do cookiebar
   * @private
   */
  _setCheckboxBehavior() {
    this.component
      .querySelectorAll(selectors.PARENT_CHECKBOX)
      .forEach((trigger) => {
        this.checkgroupBehavior = new Checkgroup(trigger)
        this.checkgroupBehavior.setBehavior()
      })
  }

  /**
   * Trata da seleção dos checkboxes
   * @private
   */
  _setSelectionBehavior() {
    this.component.querySelectorAll(selectors.CHECKBOX).forEach((checkbox) => {
      checkbox.addEventListener('change', this._controlSelection.bind(this))
    })
  }

  /**
   * Handler para o evento change na seleção dos checkboxes
   * @param {object} event - Objeto eventDOM
   * @private
   */
  _controlSelection(event) {
    const segment = event.currentTarget.id.split('-')
    switch (segment[1]) {
      case 'all':
        this._setCheckAllBehavior(event.currentTarget)
        break
      case 'group':
        this._setCheckgroupBehavior(event.currentTarget, segment[2])
        break
      case 'cookie':
        this._setCheckCookieBehavior(
          event.currentTarget,
          segment[2],
          segment[3]
        )
        break
      default:
    }
  }

  /**
   * Trata a seleção do checkbox geral
   * @param {object} checkbox - Elemento DOM que represeta um checkbox geral
   * @private
   */
  _setCheckAllBehavior(checkbox) {
    this.data.selectAll = checkbox.checked
    this.data.allIndeterminated = checkbox.hasAttribute('indeterminate')
      ? true
      : false
    this._displayBroadAlertMessage()
  }

  /**
   * Trata da seleção do checkbox de grupo
   * @param {object} checkbox - Elemento DOM que represta um checkbox de grupo
   * @param {number} groupIndex - Índice do grupo
   * @private
   */
  _setCheckgroupBehavior(checkbox, groupIndex) {
    this.data.cookieGroups[groupIndex].groupSelected = checkbox.checked
    this.data.cookieGroups[groupIndex].groupIndeterminated =
      checkbox.hasAttribute('indeterminate') ? true : false
    this.data.cookieGroups[groupIndex].cookieList.forEach(
      (cookieData, cookieIndex) => {
        if (!cookieData.cookieOptOut) {
          cookieData.cookieSelected = checkbox.checked
          this._displayCookieAlertMessage(groupIndex, cookieIndex)
        }
      }
    )
    this._displayGroupAlertMessage(groupIndex)
  }

  /**
   * Trata da seleção do checkbox de cookie
   * @param {object} checkbox - Elemento DOM que represeta um checkbox de cookie
   * @param {number} groupIndex - Índice do grupo
   * @param {number} cookieIndex - Índicd do cookie dentro do grupo
   * @private
   */
  _setCheckCookieBehavior(checkbox, groupIndex, cookieIndex) {
    this.data.cookieGroups[groupIndex].cookieList[cookieIndex].cookieSelected =
      checkbox.checked
    this._displayCookieAlertMessage(groupIndex, cookieIndex)
  }

  /**
   * Controla a apresentação da mensagem geral
   * @private
   */
  _displayBroadAlertMessage() {
    this.component
      .querySelectorAll(selectors.BROAD_ALERT)
      .forEach((broadAlert) => {
        if (
          this.data.allAlertMessage &&
          (!this.data.selectAll || this.data.allIndeterminated)
        ) {
          broadAlert.classList.remove('d-none')
        } else {
          broadAlert.classList.add('d-none')
        }
      })
  }

  /**
   * Controla a apresentação da mensagem de grupo
   * @param {number} groupIndex - Índice do grupo
   * @private
   */
  _displayGroupAlertMessage(groupIndex) {
    const group = this.component.querySelectorAll(selectors.GROUP_INFO)[
      groupIndex
    ]
    group.querySelectorAll(selectors.GROUP_ALERT).forEach((groupAlert) => {
      if (
        this.data.cookieGroups[groupIndex].groupAlertMessage &&
        (!this.data.cookieGroups[groupIndex].groupSelected ||
          this.data.cookieGroups[groupIndex].groupIndeterminated)
      ) {
        groupAlert.classList.remove('d-none')
      } else {
        groupAlert.classList.add('d-none')
      }
    })
  }

  /**
   * Controla a apresentação da mensagem de cookie
   * @param {number} groupIndex - Índice do grupo
   * @param {number} cookieIndex - Índice do cookie dentro do grupo
   */
  _displayCookieAlertMessage(groupIndex, cookieIndex) {
    const group = this.component.querySelectorAll(selectors.GROUP_INFO)[
      groupIndex
    ]
    const cookie = group.nextElementSibling.querySelectorAll(
      selectors.COOKIE_CARD
    )[cookieIndex]
    cookie.querySelectorAll(selectors.COOKIE_ALERT).forEach((cookieAlert) => {
      if (
        this.data.cookieGroups[groupIndex].cookieList[cookieIndex]
          .alertMessage &&
        !this.data.cookieGroups[groupIndex].cookieList[cookieIndex]
          .cookieSelected
      ) {
        cookieAlert.classList.remove('d-none')
      } else {
        cookieAlert.classList.add('d-none')
      }
    })
  }

  /**
   * Busca um elemento DOM pai com uma determinada classe
   * @param {object} element - Elemento DOM
   * @param {string} className - Nome de uma classe para busca
   * @returns {object} - Elemento DOM representando que contém uma determinada classe
   * @private
   */
  _getParentElementByClass(element, className) {
    parent = element.parentNode
    while (!parent.classList.contains(className)) {
      parent = parent.parentNode
    }
    return parent
  }

  /**
   * Troca a classe do icone
   * @param {object} element - Elemento DOM referente ao icone
   * @param {string} oldIcon - Classe do icone que será retirada
   * @param {string} newIcon - Classe do icone que será incluido
   * @private
   */
  _toggleIcon(element, oldIcon, newIcon) {
    element.querySelectorAll(selectors.BUTTON_ICON).forEach((icon) => {
      icon.classList.remove(oldIcon)
      icon.classList.add(newIcon)
    })
  }

  /**
   * Trata a label do atributo title e aria-label
   * @param {object} element - Elemento DOM referente ao grupo
   * @param {string} label - Label para o title e aria-label
   * @private
   */
  _setGroupAttributes(element, label) {
    element
      .querySelectorAll(
        `${`${selectors.GROUP_BUTTON}, ${selectors.GROUP_NAME}, ${selectors.COOKIES_CHECKED}, ${selectors.GROUP_SIZE}`}`
      )
      .forEach((item) => {
        item.setAttribute('title', label)
        item.setAttribute('aria-label', label)
      })
  }

  /**
   * Trata a rolagem da tela do grupo de cookies aberto
   * @param {object} element - Elemento DOM que representa a grupo de cookies
   * @private
   */
  _scrollUp(element) {
    setTimeout(() => {
      this.component.querySelectorAll(selectors.WRAPPER).forEach(() => {
        setTimeout(() => {
          element.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
          })
        }, 150)
      }, 5000)
    })
  }

  /**
   * Mostra o cookiebar na tela com foco e no modo escolhido
   * @private
   */
  _showCookiebar() {
    this.component.classList.remove('d-none')
    this.component.focus()
    switch (this.mode) {
      case 'open':
        this.component.classList.remove('default')
        this.component
          .querySelectorAll(selectors.POLITICS_BUTTON)
          .forEach((button) => {
            button.classList.add('d-none')
          })
        document.body.style.overflowY = 'hidden'
        this._setOpenView()
      default:
    }
  }

  /**
   * Oculta o cookiebar na tela
   * @private
   */
  _hideCookiebar() {
    this.component.classList.add('d-none')
  }

  /**
   * Configura a altura da parte rolável do cookiebar de acordo com a altura da janela
   * @private
   */
  _setOpenView() {
    const wrapper = this.component.querySelector(selectors.WRAPPER)
    const containerFluid = this.component.querySelector(
      selectors.CONTAINER_FLUID
    )
    const modalFooter = this.component.querySelector(selectors.MODAL_FOOTER)
    const padding = window
      .getComputedStyle(containerFluid, null)
      .getPropertyValue('padding-top')
      .match(/\d+/)
    const height = `${
      window.innerHeight - padding * 2 - modalFooter.offsetHeight
    }px`
    wrapper.style.height = height
  }

  /**
   * Configura a altura do cookiebar no modo default
   * @private
   */
  _setDefaultView() {
    this.component.querySelector(selectors.WRAPPER).removeAttribute('style')
  }

  /**
   * Cria o JSON de saída do cookiebar
   * @returns {string} - JSON de saída do cookiebar
   * @private
   */
  _setOutputJSON() {
    this.output = {}
    this.output.selectAll = this.data.allIndeterminated
      ? 'indeterminated'
      : this.data.selectAll
    this.output.cookieGroups = []
    this.data.cookieGroups.forEach((groupData) => {
      const cookies = []
      groupData.cookieList.forEach((cookieData) => {
        cookies.push({
          cookieId: cookieData.cookieId,
          cookieSelected: cookieData.cookieSelected,
        })
      })
      this.output.cookieGroups.push({
        cookieList: cookies,
        groupId: groupData.groupId,
        groupSelected: groupData.groupIndeterminated
          ? 'indeterminated'
          : groupData.groupSelected,
      })
    })
    return JSON.stringify(this.output)
  }

  static createCookiebar(json, callback) {
    const brCookiebar = document.createElement('div')
    brCookiebar.classList.add('br-cookiebar', 'default', 'd-none')
    brCookiebar.setAttribute('tabindex', 1)

    document.body.appendChild(brCookiebar)

    const params = {
      callback,
      component: brCookiebar,
      json,
      lang: 'pt-br',
      mode: 'default',
      name: 'br-cookiebar',
    }

    return new BRCookiebar(params)
  }
}
