import Collapse from '../../partial/js/behavior/collapse'
import Dropdown from '../../partial/js/behavior/dropdown'

/** Classe para instanciar um objeto BRTable*/
/* eslint-disable complexity */
class BRTable {
  /**
   * Instancia do objeto
   * @param {string} name - Nome do componente em minúsculo
   * @param {object} component - Objeto referenciando a raiz do componente DOM
   * @param {number} sequence - 'índice do componente para sobreposição'
   */
  constructor(name, component, sequence) {
    this.name = name
    this.component = component
    this._header = this.component.querySelector('.header, .table-header')
    this._table = this.component.querySelector('table')
    this._sequence = sequence
    this._setBehaviors()
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehaviors() {
    this._makeResponsiveTable()
    this._setHeaderWidth()
    this._searchBehavior()
    this._dropdownBehavior()
    this._collpaseBehavior()
    this._densityBehavior()
    this._setClickActions()
    this._getBRHeaderHeight()
  }

  /**
   * Configura a altura do cabeçalho
   * @private
   */
  _getBRHeaderHeight() {
    const BRHeader = document.querySelector('.br-header')
    if (BRHeader) {
      window.addEventListener('scroll', () => {
        this._header.style.top = `${BRHeader.clientHeight}px`
      })
    }
  }

  /**
   * Configura reponsividade da tabela
   * @private
   */
  _makeResponsiveTable() {
    const responsiveClass = 'responsive'
    if (!this.component.querySelector(`.${responsiveClass}`)) {
      const responsiveElement = document.createElement('div')
      responsiveElement.classList.add(responsiveClass)
      responsiveElement.appendChild(this._table)
      this._header.after(responsiveElement)
    }
  }

  /**
   * Configura rolagem
   * @private
   */
  _makeScroller() {
    const scrollerTag = document.createElement('div')
    scrollerTag.classList.add('scroller')
    for (const header of this._table.querySelectorAll('thead tr th')) {
      const clonedHeader = document.createElement('div')
      clonedHeader.classList.add('item')
      clonedHeader.innerHTML = header.innerHTML
      if (header.offsetWidth) {
        clonedHeader.style.flex = `1 0 ${header.offsetWidth}px`
      }
      scrollerTag.appendChild(clonedHeader)
      const checkbox = clonedHeader.querySelector('.br-checkbox')
      if (checkbox) {
        const input = checkbox.querySelector('input')
        const label = checkbox.querySelector('label')
        input.id = `${input.id}-clone`
        label.setAttribute('for', input.id)
      }
    }
    return scrollerTag
  }

  /**
   * Configura largura do cabeçalho
   * @private
   */
  _setHeaderWidth() {
    for (const clonedHeader of this.component.querySelectorAll(
      '.headers > div'
    )) {
      for (const [index, header] of this.component
        .querySelectorAll('table thead tr th')
        .entries()) {
        clonedHeader.children[index].style.flex = `1 0 ${header.offsetWidth}px`
      }
    }
  }

  /**
   * Configura coportamento do dropdown
   * @private
   */
  _dropdownBehavior() {
    this.component
      .querySelectorAll('[data-toggle="dropdown"]')
      .forEach((trigger) => {
        const config = {
          iconToHide: 'fa-chevron-up',
          iconToShow: 'fa-chevron-down',
          trigger,
          useIcons: true,
        }
        const dropdown = new Dropdown(config)
        dropdown.setBehavior()
      })
  }

  /**
   * Configura comportamento de colapsar
   * @private
   */
  _collpaseBehavior() {
    this.component
      .querySelectorAll('[data-toggle="collapse"]')
      .forEach((trigger) => {
        const config = {
          iconToHide: 'fa-chevron-up',
          iconToShow: 'fa-chevron-down',
          trigger,
          useIcons: true,
        }
        const collapse = new Collapse(config)
        collapse.setBehavior()
      })
  }

  /**
   * Configura comportamento da busca
   * @private
   */
  _searchBehavior() {
    if (this.component.dataset.search) {
      const trigger = this.component.querySelector('[data-toggle="search"]')
      const target = this.component.querySelector('.search-bar')
      const dismiss = this.component.querySelector('[data-dismiss="search"]')

      // Inicializar
      this._searchInit(trigger)

      // Abre busca
      trigger.addEventListener('click', () => {
        return this._searchOpen(trigger, target)
      })

      // Fecha busca
      dismiss.addEventListener('click', () => {
        return this._searchClose(trigger, target)
      })
      target.querySelector('input').addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
          this._searchClose(trigger, target)
        }
      })
    }
  }

  /**
   * Inicializa a busca
   * @private
   * @param {object} trigger - Objeto referente ao elemento que dispara a ação
   */
  _searchInit(trigger) {
    trigger.setAttribute('aria-expanded', 'false')
  }

  /**
   * Abre a busca
   * @private
   * @param {object} trigger - Objeto referente ao elemento que dispara a ação
   * @param {object} target - Objeto referente ao alvo da ação
   */
  _searchOpen(trigger, target) {
    trigger.setAttribute('aria-expanded', 'true')
    target.classList.add('show')
    target.parentElement.classList.add('show')
    target.querySelector('input').focus()
  }

  /**
   * Fecha a busca
   * @private
   * @param {object} trigger - Objeto referente ao elemento que dispara a ação
   * @param {object} target - Objeto referente ao alvo da ação
   */
  _searchClose(trigger, target) {
    target.querySelector('input').value = ''
    target.classList.remove('show')
    target.parentElement.classList.remove('show')
    trigger.focus()
    trigger.setAttribute('aria-expanded', 'false')
  }

  /**
   * Configura densidades
   * @private
   */
  _densityBehavior() {
    const desityTriggers = this.component.querySelectorAll('[data-density]')
    for (const desityTrigger of desityTriggers) {
      desityTrigger.addEventListener('click', () => {
        this.component.classList.remove('small', 'medium', 'large')
        this.component.classList.add(desityTrigger.dataset.density)
        this._dropdownClose(
          desityTrigger
            .closest('.dropdown')
            .querySelector('[data-toggle="dropdown"]')
        )
      })
    }
  }

  /**
   * Configura ações de clique
   * @private
   */
  _setClickActions() {
    const headerCheckbox = this.component.querySelector(
      '.headers [type="checkbox"]'
    )
    const tableCheckboxes = this.component.querySelectorAll(
      'tbody [type="checkbox"]'
    )
    const selectedBar = this.component.querySelector('.selected-bar')
    const checkAlls = this.component.querySelectorAll(
      '[data-toggle="check-all"]'
    )
    for (const checkAll of checkAlls) {
      checkAll.addEventListener('click', () => {
        this._checkAllTable(selectedBar, tableCheckboxes, headerCheckbox)
        if (checkAll.parentElement.classList.contains('br-list')) {
          this._dropdownClose(
            checkAll
              .closest('.dropdown')
              .querySelector('[data-toggle="dropdown"]')
          )
        }
      })
    }
    if (tableCheckboxes) {
      for (const checkbox of tableCheckboxes) {
        checkbox.addEventListener('change', () => {
          this._checkRow(checkbox, selectedBar, tableCheckboxes, headerCheckbox)
        })
      }
    }
  }

  /**
   * Configura seleção da linha
   * @private
   * @param {object} checkbox - Objeto referente ao checkbox
   * @param {boolean} check - define se a linha deve ser selecionada
   */
  _setRow(checkbox, check) {
    const tr = checkbox.parentNode.parentNode.parentNode
    if (check) {
      tr.classList.add('is-selected')
      checkbox.parentNode.classList.add('is-inverted')
      checkbox.checked = true
    } else {
      tr.classList.remove('is-selected')
      checkbox.parentNode.classList.remove('is-inverted')
      checkbox.checked = false
    }
  }

  /**
   * Configura seleção da linha
   * @private
   * @param {object} checkbox - Objeto referente ao checkbox
   * @param {object} selectedBar - Objeto referente a barra contextual
   * @param {object} tableCheckboxes - Objeto referente a lista de checkboxes
   * @param {object} headerCheckbox - Objeto referente ao checkbox do header
   */
  _checkRow(checkbox, selectedBar, tableCheckboxes, headerCheckbox) {
    const check = checkbox.checked
    this._setRow(checkbox, check)
    this._setSelectedBar(
      check ? 1 : -1,
      selectedBar,
      tableCheckboxes,
      headerCheckbox
    )
  }

  /**
   * Seleciona todas as linhas
   * @private
   * @param {object} tableCheckboxes - Objeto referente a lista de checkboxes
   */
  _checkAllRows(tableCheckboxes) {
    for (const checkbox of tableCheckboxes) {
      this._setRow(checkbox, true)
    }
  }

  /**
   * Desseleciona todas as linhas
   * @private
   * @param {object} tableCheckboxes - Objeto referente a lista de checkboxes
   */
  _uncheckAllRows(tableCheckboxes) {
    for (const checkbox of tableCheckboxes) {
      this._setRow(checkbox, false)
    }
  }

  /**
   * Seleciona toda a tabela
   * @private
   * @param {object} selectedBar - Objeto referente a barra contextual
   * @param {object} tableCheckboxes - Objeto referente a lista de checkboxes
   * @param {object} headerCheckbox - Objeto referente ao checkbox do header
   */
  _checkAllTable(selectedBar, tableCheckboxes, headerCheckbox) {
    let count = tableCheckboxes.length
    const infoCount = selectedBar.querySelector('.info .count')
    const total = parseInt(infoCount.innerHTML, 10)
    if (total === count) {
      this._uncheckAllRows(tableCheckboxes)
      count = -1 * count
    } else {
      this._checkAllRows(tableCheckboxes)
    }
    this._setSelectedBar(count, selectedBar, tableCheckboxes, headerCheckbox)
  }

  /**
   * Define visualização dos itens selecionados na barra contextual
   * @private
   * @param {number} count - número de itens selecionados
   * @param {object} selectedBar - Objeto referente a barra contextual
   * @param {object} tableCheckboxes - Objeto referente a lista de checkboxes
   * @param {object} headerCheckbox - Objeto referente ao checkbox do header
   */
  _setSelectedBar(count, selectedBar, tableCheckboxes, headerCheckbox) {
    const infoCount = selectedBar.querySelector('.info .count')
    const infoText = selectedBar.querySelector('.info .text')
    const total = count < 2 ? parseInt(infoCount.innerHTML, 10) + count : count
    if (total > 0) {
      selectedBar.classList.add('show')
      infoCount.innerHTML = total
      infoText.innerHTML = total > 1 ? 'itens selecionados' : 'item selecionado'
      if (headerCheckbox) headerCheckbox.parentNode.classList.add('is-checking')
      if (total === tableCheckboxes.length) {
        if (headerCheckbox) {
          headerCheckbox.checked = true
          headerCheckbox.parentNode.classList.remove('is-checking')
        }
      }
    } else {
      infoCount.innerHTML = 0
      if (headerCheckbox) {
        headerCheckbox.checked = false
        headerCheckbox.parentNode.classList.remove('is-checking')
      }
      selectedBar.classList.remove('show')
    }
  }
}

export default BRTable
