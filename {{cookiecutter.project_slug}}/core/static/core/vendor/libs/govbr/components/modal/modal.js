import BRScrim from '../scrim/scrim'

/** Classe para instanciar um objeto BRModal*/
class BRModal {
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
    for (const brScrim of window.document.querySelectorAll('.br-scrim')) {
      const scrim = new BRScrim('br-scrim', brScrim)
      for (const button of window.document.querySelectorAll(
        '.br-scrim + button'
      )) {
        button.addEventListener('click', () => {
          scrim.showScrim()
        })
      }
    }
  }
}

export default BRModal
