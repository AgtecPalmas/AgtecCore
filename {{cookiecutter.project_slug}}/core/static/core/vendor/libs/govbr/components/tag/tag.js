/** Classe para instanciar um objeto BRTag*/
class BRTag {
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
    if (this.component.classList.contains('interaction-select')) {
      // Inicializa selecionado
      if (this.component.querySelector('input').getAttribute('checked')) {
        this.component.classList.add('selected')
      }
      this._setSelection()
    }
    this._closeTag()
    this._dismissTag()
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setSelection() {
    const label = this.component.querySelector('label')
    const input = this.component.querySelector('input')
    // const tagRadio = input.getAttribute('type') === 'radio' ? true : false

    label.addEventListener('click', (event) => {
      this._toggleSelection(input, event)
    })
    input.addEventListener('keydown', (event) => {
      if (event.code === 'Space' || event.code === 'Enter') {
        this._toggleSelection(input, event)
      }
    })
  }

  /**
   * Muda estado do radio
   * @private
   * @param {object} input - referencia DOM ao input
   */
  _toggleRadio(input) {
    if (this.component.querySelector('[type="radio"')) {
      const nameTag = input.getAttribute('name')
      for (const tagRadio of window.document.querySelectorAll(
        `[name=${nameTag}]`
      )) {
        this._removeCheck(tagRadio)
      }
    }
  }

  /**
   * Muda estado do input
   * @private
   * @param {object} input - referencia DOM ao input
   * @param {event} event - ação que disparou o evento
   */
  _toggleSelection(input, event) {
    event.preventDefault()
    this._toggleRadio(input)
    if (input.getAttribute('checked')) {
      this._removeCheck(input)
      return
    }

    this._setCheck(input)
  }

  /**
   * Define estado do input para selecionado
   * @private
   * @param {object} input - referencia DOM ao input
   */
  _setCheck(input) {
    input.setAttribute('checked', 'checked')
    input.parentElement.classList.add('selected')
  }

  /**
   * Define estado do input para desselecionado
   * @private
   * @param {object} input - referencia DOM ao input
   */
  _removeCheck(input) {
    input.removeAttribute('checked')
    input.parentElement.classList.remove('selected')
  }

  /**
   * Define comportamento do botão de fechar usando classe (compatibilidade)
   * @private
   */
  _closeTag() {
    const closeBtn = this.component.querySelector('.br-button.close')

    if (closeBtn) {
      const brTag = closeBtn.closest('.br-tag')

      brTag.addEventListener('click', () => {
        closeBtn.closest('.br-tag').remove()
      })
    }
  }

  /**
   * Define comportamento do botão de fechar usando data-dismiss
   * @private
   */
  _dismissTag() {
    this.component.querySelectorAll('[data-dismiss]').forEach((closeBtn) => {
      closeBtn.addEventListener('click', () => {
        const target = document.querySelector(
          `#${closeBtn.getAttribute('data-dismiss')}`
        )
        if (target) target.remove()
      })
    })
  }
}

const tagList = []
for (const brTag of window.document.querySelectorAll('.br-tag')) {
  tagList.push(new BRTag('br-tab', brTag))
}

export default BRTag
