/** Classe para instanciar um objeto BRAlert */
class BRAlert {
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
    for (const button of this.component.querySelectorAll(
      '.br-message .close'
    )) {
      button.addEventListener('click', () => {
        this._dismiss(this.component)
      })
    }
  }

  /**
   * Desvincula a instancia do objeto
   * @private
   * @param {object} component - Objeto referenciando a raiz do componente DOM
   */
  _dismiss(component) {
    component.parentNode.removeChild(component)
  }
}

export default BRAlert
