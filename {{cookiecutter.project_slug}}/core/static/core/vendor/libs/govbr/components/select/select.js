/**
 * Classe do componente BRSelect
 */

class BRSelect {
  /**
   * Instancia o componente
   * @property {string} name - Nome do componente em minúsculo
   * @property {object} component - Objeto referenciando a raiz do componente DOM
   * @property {string} notFound - (Opcional) String contendo código html para informar que a busca não encontrou nenhuma opção.
   *                                Se não informado, será usado um código html padrão.
   */

  constructor(name, component, notFound) {
    this.name = name
    this.component = component
    this.notFound = notFound
    this.multiple = component.hasAttribute('multiple')
    this._setOptionsList()
    this._setBehavior()
  }
  /**
   * Retorna os valores dos elementos selecionados
   * @returns {Object[]} elementos selecionados
   *
   */
  get selected() {
    return this._optionSelected('value')
  }
  /**
   * Retorna os elementos selecionados pelo inputValue
   * @param {Object[]} elementos selecionados
   * @returns
   */
  get selectedValue() {
    return this._optionSelected('inputValue')
  }

  /**
   * Retorna os elementos options selecionados
   * @param {Object[]} elementos selecionados
   * @returns
   */
  _optionSelected(strOption) {
    let selected = []
    for (const [index, option] of this.optionsList.entries()) {
      if (!this.multiple) {
        if (option.selected) {
          selected = option[strOption]
          break
        }
      } else {
        if (index > 0 && option.selected) {
          selected.push(option[strOption])
        }
      }
    }
    return selected
  }

  /**
   * Remove o elemento que indica item não encontrado
   * @private
   */
  _removeNotFoundElement() {
    const list = this.component.querySelector('.br-list')
    if (list.querySelector('.br-item.not-found')) {
      list.removeChild(list.querySelector('.br-item.not-found'))
    }
  }

  /**
   * Coloca o texto Item não encontrado no select
   * @private
   */
  _addNotFoundElement() {
    const image = `data:image/png;base64,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`
    const notFoundElement = `
      <div class="br-item not-found">
        <div class="container pl-0 pr-0">
          <div class="row">
            <div class="col-auto">
              <img src="${image}">
            </div>
            <div class="col">
              <p><strong>Ops!</strong> Não encontramos o que você está procurando!</p>
            </div>
          </div>
        </div>
      </div>
    `
    const list = this.component.querySelector('.br-list')
    list.insertAdjacentHTML(
      'beforeend',
      this.notFound ? this.notFound : notFoundElement
    )
  }
  /**
   * Cria listagem de elementos do select
   * @private
   */
  _setOptionsList() {
    this.optionsList = []
    for (const item of this.component.querySelectorAll('.br-list .br-item')) {
      for (const input of item.querySelectorAll(
        '.br-radio input, .br-checkbox input'
      )) {
        const option = {
          element: item,
          focus: false,
          inputValue: input.value,
          selected: false,
          value: input.nextElementSibling.innerText,
          visible: true,
        }
        this.optionsList.push(option)
      }
    }
  }
  /**
   * Reseta estado da lista
   * @private
   */
  resetOptionsList() {
    this._unsetSelectionBehavior()
    this._setOptionsList()
    this._setSelectionBehavior()
  }
  /**
   * Define o comportamento do componente
   * @private
   */
  _setBehavior() {
    this._setSearchIcon()
    this._setDropdownBehavior()
    this._setKeyboardBehavior()
    this._setSelectionBehavior()
    this._setFilterBehavior()
  }
  /**
   * Define o comportamento de dropdown
   * @private
   */

  _setDropdownBehavior() {
    for (const input of this.component.querySelectorAll(
      '.br-input input[type="text"]'
    )) {
      input.addEventListener('focus', () => {
        this._openSelect()
        this._resetFocus()
      })
    }
    for (const trigger of this.component.querySelectorAll(
      '.br-input .br-button[data-trigger]'
    )) {
      trigger.addEventListener('click', () => {
        for (const list of this.component.querySelectorAll('.br-list')) {
          if (list.hasAttribute('expanded')) {
            this._closeSelect()
          } else {
            this._openSelect()
          }
        }
      })
    }
    window.document.addEventListener('click', (event) => {
      if (!this.component.contains(event.target)) {
        this._closeSelect()
      }
    })
  }
  /**
   * Define o comportamento de teclado
   * @private
   */

  _setKeyboardBehavior() {
    for (const input of this.component.querySelectorAll(
      '.br-input input[type="text"]'
    )) {
      input.addEventListener('keydown', this._handleKeydownOnInput.bind(this))
    }
    for (const list of this.component.querySelectorAll('.br-list')) {
      // eslint-disable-next-line complexity
      list.addEventListener('keydown', this._handleKeydownOnList.bind(this))
    }
  }
  /**
   * Retira o comportamento de teclado
   * @private
   */

  _unsetKeyboardBehavior() {
    for (const input of this.component.querySelectorAll(
      '.br-input input[type="text"]'
    )) {
      input.removeEventListener('keydown', this._handleKeydownOnInput, false)
    }
    for (const list of this.component.querySelectorAll('.br-list')) {
      // eslint-disable-next-line complexity
      list.addEventListener('keydown', this._handleKeydownOnList.bind(this))
    }
  }

  /**
   * Verifica a navegação
   * @param {object} event evento que foi ativado
   * @private
   */
  _handleKeydownOnInput(event) {
    //Close Select
    if (event.shiftKey && event.key === 'Tab') {
      this._closeSelect()
      this._resetFocus()
    }
    if (event.key === 'Tab' && !event.shiftKey) {
      event.target.parentNode.querySelector('.br-button').focus()
    }
    if (event.keyCode === 40) {
      event.preventDefault()
      for (const list of this.component.querySelectorAll('.br-list')) {
        list.focus()
        if (list === document.activeElement) {
          this._getNextItem().focus()
        }
      }
    }
  }
  /**
   * Define comportamentos de teclado na lista
   * @private
   */

  _handleKeydownOnList(event) {
    event.preventDefault()
    switch (event.keyCode) {
      case 9:
        this._closeSelect()
        this._resetFocus()
        break
      case 27:
        this._closeSelect()
        break
      case 32:
        this._setKeyClickOnOption(event.currentTarget)
        break
      case 38:
        this._getPreviousItem().focus()
        break
      case 40:
        this._getNextItem().focus()
        break
      default:
        break
    }
  }
  /**
   * Define comportamentos de teclado no option
   * @private
   */
  _setKeyClickOnOption(list) {
    for (const [index, item] of list.querySelectorAll('.br-item').entries()) {
      if (this.optionsList[index].focus) {
        for (const check of item.querySelectorAll(
          '.br-radio input[type="radio"], .br-checkbox input[type="checkbox"]'
        )) {
          check.click()
          this._sendEvent()
        }
      }
    }
  }

  /**
   * Envia o evento onchange
   * @private
   */
  _sendEvent() {
    const clickEvent = new CustomEvent('onChange', {
      bubbles: true,
      detail: this.component,
    })
    this.component.dispatchEvent(clickEvent)
  }

  /**
   * preseleciona o elemento apartir da classe css .selected
   * @private
   */
  _setDefaultSelected() {
    const selectedItems = this.component.querySelectorAll('.br-list .selected')

    const iterable = typeof selectedItems[Symbol.iterator]
    if (selectedItems !== null && iterable === 'function') {
      for (const item of selectedItems) {
        this._setSelected(this._positionSelected(item), item)
      }
    }
  }

  /**
   * Retorna posição do elemento no select
   * @param {element} component elemento que vai ser pesquisado
   * @returns {integer} valor da posição
   */
  _positionSelected(component) {
    for (const [index, componente] of this.component
      .querySelectorAll('.br-list .br-item')
      .entries()) {
      if (componente === component) {
        return index
      }
    }
    return 0
  }
  /**
   * Desfine comportamento do clique no checkbox
   * @param {int} index
   * @param {object} item -  Objeto do item clicado
   * @param {object} event  -  Objeto do evento do clique
   * @private
   */
  _handleClickOnCheck(index, item, event) {
    if (!this.multiple) {
      for (const [index2, item2] of this.component
        .querySelectorAll('.br-list .br-item')
        .entries()) {
        this._removeSelected(index2, item2)
      }
      this._setSelected(index, item)
      this._closeSelect()
    } else if (event.currentTarget.hasAttribute('checked')) {
      this._removeSelected(index, item)
    } else {
      this._setSelected(index, item)
    }
    if (item.hasAttribute('data-all')) {
      for (const check of item.querySelectorAll(
        '.br-checkbox input[type="checkbox"]'
      )) {
        if (!check.hasAttribute('checked')) {
          this._setAttribute()
          item.querySelectorAll('label')[0].innerText = 'Selecionar Todos'
        } else {
          for (const item2 of this.component.querySelectorAll(
            '.br-list .br-item'
          )) {
            for (const check2 of item2.querySelectorAll(
              '.br-checkbox input[type="checkbox"]'
            )) {
              if (!check2.hasAttribute('checked')) {
                check2.click()
              }
            }
          }
          item.querySelectorAll('label')[0].innerText = 'Deselecionar Todos'
        }
      }
    }
    this._sendEvent()
  }
  /**
   * Define comportamentos na seleção
   * @private
   */
  _setSelectionBehavior() {
    this.selectionHandler = []
    this._setDefaultSelected()
    for (const [index, item] of this.component
      .querySelectorAll('.br-list .br-item')
      .entries()) {
      for (const check of item.querySelectorAll(
        '.br-radio input[type="radio"], .br-checkbox input[type="checkbox"]'
      )) {
        this.selectionHandler.push({
          element: check,
          handler: this._handleClickOnCheck.bind(this, index, item),
        })
        check.addEventListener('click', this.selectionHandler[index].handler)
      }
    }
  }
  /**
   * retira comportamento  de clique na seleção
   * @private
   */
  _unsetSelectionBehavior() {
    this.selectionHandler.forEach((item) => {
      item.element.removeEventListener('click', item.handler, false)
    })
  }
  /**
   * Define comportamentos no filtro do input
   * @private
   */
  _setFilterBehavior() {
    for (const input of this.component.querySelectorAll(
      '.br-input input[type="text"]'
    )) {
      input.addEventListener('input', (event) => {
        let allHidden = true
        this._filter(event.currentTarget.value)
        for (const option of this.optionsList) {
          if (option.visible) {
            allHidden = false
          }
        }

        if (allHidden) {
          // event.currentTarget.value = event.currentTarget.value.slice(0, -1)
          this._filter(event.currentTarget.value)
        }
      })
    }
  }
  /**
   * Define filtro no list
   * @private
   */
  _filter(value) {
    let hasVisible = false
    for (const [index, item] of this.component
      .querySelectorAll('.br-list .br-item')
      .entries()) {
      this._removeNotFoundElement()
      if (!this.optionsList[index]) {
        continue
      }
      if (
        this.optionsList[index].value
          .toUpperCase()
          .indexOf(value.toUpperCase()) === -1
      ) {
        item.classList.add('d-none')
        this.optionsList[index].visible = false
      } else {
        item.classList.remove('d-none')
        this.optionsList[index].visible = true
        hasVisible = true
      }
    }
    if (hasVisible === false) {
      this._addNotFoundElement()
    }
  }
  /**
   * Define atributo checked com click
   * @private
   */
  _setAttribute() {
    for (const item2 of this.component.querySelectorAll('.br-list .br-item')) {
      for (const check2 of item2.querySelectorAll(
        '.br-checkbox input[type="checkbox"]'
      )) {
        if (check2.hasAttribute('checked')) {
          check2.click()
        }
      }
    }
  }

  /**
   * Seleciona o elemento e retira checked dos outros elementos
   * @param {integer} index Posição do elemento na lista
   * @param {*} item elemento em que vai ser selecionado
   * @private
   */
  _setSelected(index, item) {
    item.classList.add('selected')
    for (const check of item.querySelectorAll('.br-radio, .br-checkbox')) {
      for (const input of check.querySelectorAll(
        'input[type="radio"], input[type="checkbox"]'
      )) {
        input.setAttribute('checked', '')
      }
    }
    this.optionsList[index].selected = true
    this._setInput()
  }

  /**
   * Retira o estado selecionado do elemento
   * @param {integer} index Posição do elemento na lista
   * @param {*} item elemento em que vai ser desselecionado
   * @private
   */
  _removeSelected(index, item) {
    item.classList.remove('selected')
    for (const check of item.querySelectorAll('.br-radio, .br-checkbox')) {
      for (const input of check.querySelectorAll(
        'input[type="radio"], input[type="checkbox"'
      )) {
        input.removeAttribute('checked')
      }
      this.optionsList[index].selected = false
      this._setInput()
    }
  }
  /**
   * Determina o input
   * @private
   */
  _setInput() {
    for (const input of this.component.querySelectorAll(
      '.br-input input[type="text"]'
    )) {
      if (!this.multiple) {
        input.value = this.selected
      } else if (this.selected.length === 0) {
        input.value = ''
      } else {
        this.mountSelectedValues(input)
      }
    }
  }
  /**
   * Monta a string apresentada no campo input do multiselect
   * @param {object} input Referencia o elemento input do select
   */
  mountSelectedValues(input) {
    const GAP = 0.4
    let amount = 1
    let value = this.selected.toString().replaceAll(',', ', ')
    const tempSpan = document.createElement('span')
    tempSpan.innerHTML = value
    document.querySelector('body').insertAdjacentElement('beforeend', tempSpan)

    while (tempSpan.offsetWidth > input.offsetWidth - input.offsetWidth * GAP) {
      value = this.selected
        .slice(0, this.selected.length - amount)
        .toString()
        .replaceAll(',', ', ')
        .concat(` + (${amount})`)
      tempSpan.innerHTML = value
      amount++
    }
    input.value = value

    tempSpan.remove()
  }
  /**
   * Retorna elemento posterior ao focado
   * @returns {object}
   * @private
   */
  // eslint-disable-next-line complexity
  _getNextItem() {
    const list = this.component.querySelectorAll('.br-list .br-item')
    let iFocused
    let iVisible
    for (iFocused = 0; iFocused < this.optionsList.length; iFocused++) {
      if (this.optionsList[iFocused].focus) {
        for (
          iVisible = iFocused + 1;
          iVisible < this.optionsList.length;
          iVisible++
        ) {
          if (this.optionsList[iVisible].visible) {
            break
          }
        }
        break
      }
    }
    if (iFocused === this.optionsList.length) {
      for (const [index, option] of this.optionsList.entries()) {
        if (option.visible) {
          option.focus = true
          return list[index]
        }
      }
    } else if (iVisible < this.optionsList.length) {
      this.optionsList[iFocused].focus = false
      this.optionsList[iVisible].focus = true
      return list[iVisible]
    } else {
      return list[iFocused]
    }
    return ''
  }
  /**
   * Retorna elemento anterior ao focado
   * @returns {object}
   * @private
   */
  _getPreviousItem() {
    const list = this.component.querySelectorAll('.br-list .br-item')
    let iFocused
    let iVisible
    for (iFocused = 0; iFocused < this.optionsList.length; iFocused++) {
      if (this.optionsList[iFocused].focus) {
        for (iVisible = iFocused - 1; iVisible > 0; iVisible--) {
          if (this.optionsList[iVisible].visible) {
            break
          }
        }
        break
      }
    }
    if (iFocused === 0) {
      return list[iFocused]
    } else {
      this.optionsList[iFocused].focus = false
      this.optionsList[iVisible].focus = true
      return list[iVisible]
    }
  }
  /**
   * Reseta valor do input
   * @private
   */
  _resetInput() {
    for (const input of this.component.querySelectorAll(
      '.br-input input[type="text"]'
    )) {
      input.value = ''
    }
  }
  /**
   * Reseta o focus dos elementos
   * @private
   */
  _resetFocus() {
    for (const option of this.optionsList) {
      option.focus = false
    }
  }
  /**
   * Reseta o focus dos elementos visiveis
   * @private
   */

  _resetVisible() {
    const list = this.component.querySelectorAll('.br-list .br-item')
    for (const [index, option] of this.optionsList.entries()) {
      option.visible = true
      list[index].classList.remove('d-none')
    }
  }
  /**
   * Abre o select aberto
   * @private
   */
  _openSelect() {
    for (const list of this.component.querySelectorAll('.br-list')) {
      list.setAttribute('expanded', '')
    }
    for (const icon of this.component.querySelectorAll(
      '.br-input .br-button i'
    )) {
      icon.classList.remove('fa-angle-down')
      icon.classList.add('fa-angle-up')
    }
    this._resetInput()
  }
  /**
   * Fecha o select aberto
   * @private
   */
  _closeSelect() {
    for (const list of this.component.querySelectorAll('.br-list')) {
      list.removeAttribute('expanded')
    }
    for (const icon of this.component.querySelectorAll(
      '.br-input .br-button i'
    )) {
      icon.classList.remove('fa-angle-up')
      icon.classList.add('fa-angle-down')
    }
    this._setInput()
    this._resetFocus()
    this._resetVisible()
  }
  /**
   * Adiciona ícone de busca
   * @private
   */
  _setSearchIcon() {
    const brInput = this.component.querySelector('.br-input')
    const dropButton = this.component.querySelector('[data-trigger]')
    // Ícone de busca
    const searchIcon = document.createElement('i')
    searchIcon.classList.add('fas', 'fa-search')
    searchIcon.setAttribute('aria-hidden', 'true')
    // Container para o ícone
    const inputIcon = document.createElement('div')
    inputIcon.classList.add('input-icon')
    inputIcon.appendChild(searchIcon)
    // Estrutura para input com ícone
    const inputGroup = document.createElement('div')
    inputGroup.classList.add('input-group')
    inputGroup.appendChild(inputIcon)
    inputGroup.appendChild(brInput.querySelector('input'))
    brInput.appendChild(inputGroup)
    brInput.appendChild(dropButton)
  }
}

export default BRSelect
