/** Classe para instanciar um objeto BRTextArea*/
class BRTextArea {
  /**
   * Instancia do objeto
   * @param {string} name - Nome do componente em minúsculo
   * @param {object} component - Objeto referenciando a raiz do componente DOM
   */
  constructor(name, component) {
    this.name = name
    this.component = component
    this._setBehavior()
    this._setKeyup()
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehavior() {
    this.limit = this.component.querySelector('.limit')
    this.current = this.component.querySelector('.current')
    if (this.component.querySelector('textarea') !== null) {
      this.maximum = this.component
        .querySelector('textarea')
        .getAttribute('maxlength')
    }

    this.characters = this.component.querySelector('.characters')
    this.currentValue = this.component.querySelector('.current')
  }

  /**
   * Define ações do teclado
   * @private
   */
  _setKeyup() {
    this.component.addEventListener('keyup', () => {
      this.updateAssist()
    })

    this.component.querySelector('textarea').addEventListener('focus', () => {
      console.log('testando focus')
      this.updateAssist()
    })
  }

  updateAssist() {
    const characterCount = this.component.querySelector('textarea').textLength
    if (characterCount <= this.maximum && !this.characters) {
      if (this.limit) {
        this.limit.innerHTML = ''
      }

      const limitemax = this.maximum - characterCount
      const mensagemRestam = `Restam ${limitemax}caracteres `
      const mensagemRestamInner = `<span aria-live="polite">Restam  <strong >${limitemax}</strong > caracteres</span>`
      // this.currentValue.setAttribute('aria-label', mensagemRestam)
      if (this.currentValue) {
        // debugger
        this.currentValue.innerHTML = mensagemRestamInner
      }
    }
    // Com limite de caracteres
    if (!this.characters && this.limit) {
      if (characterCount === 0 && this.limit.innerHTML === '') {
        this.limit.innerHTML = `<span aria-live="polite">Limite máximo de <strong >${this.maximum}</strong> caracteres</span>`
        this.currentValue.innerHTML = ''
      }
    }
    // Sem limite de caracteres
    else {
      if (this.characters) {
        this.characters.innerHTML = `<span ><strong >${characterCount}</strong> caracteres digitados</span>`
      }
    }
  }
}

export default BRTextArea
