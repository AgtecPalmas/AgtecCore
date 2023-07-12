/** Classe para o comportamento scrim */
export default class Scrim {
  /**
   * Instancia um comportamento scrim
   * @param {object} - Objeto de configuração inicial para destructuring
   * @property {object} trigger - Elemento DOM que representa o acionador do comportmento scrim
   * @property {string} closeElement - Elemento Dom do trigger que fecha o scrim
   */
  constructor({ trigger, closeElement }) {
    this.trigger = trigger
    this.closeElement = this.elementHideScrim(closeElement)
    if (this.trigger) {
      this.setBehavior()
    }
  }

  /**
   * Alterna o estado de visualização do comportamento scrim
   * @private
   */
  showScrim() {
    if (this.trigger) {
      this.trigger.classList.add('active')
      this.trigger.setAttribute('data-visible', true)
      this.trigger.setAttribute('aria-expanded', true)
    }
  }
  /**
   * Alterna o estado de escondido do comportamento scrim
   * @private
   */
  hideScrim() {
    this.trigger.classList.remove('active')
    this.trigger.setAttribute('data-visible', false)
    this.trigger.setAttribute('aria-expanded', false)
  }

  /**
   * Seta o elemento Dom que vai fechar o scrim
   * @public
   */
  elementHideScrim(element) {
    if (this.trigger.querySelectorAll(element)) {
      this.trigger.querySelectorAll(element).forEach((element) => {
        this.closeElement = element
        this._setCloseClick()
      })
    }
  }

  /**
   * Adiciona listener de fechamento no elemento que fecha o scrim
   * @private
   */
  _setCloseClick() {
    this.closeElement.addEventListener('click', () => {
      this.hideScrim()
    })
  }
  /**
   * Configura o comportamento scrim
   * @public
   */
  setBehavior() {
    this.trigger.addEventListener('click', (event) => {
      if (event.target.getAttribute('data-scrim')) {
        this.hideScrim()
      }
    })
  }
}
