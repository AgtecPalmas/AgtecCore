import Checkgroup from '../../partial/js/behavior/checkgroup'

/** Classe para instanciar um objeto BRCheckbox*/
class BRCheckbox {
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
    this._setCheckgroupBehavior()
  }

  /**
   * Define comportamentos do checkgroup
   * @private
   */
  _setCheckgroupBehavior() {
    this.component
      .querySelectorAll('input[type="checkbox"][data-parent]')
      .forEach((trigger) => {
        const checkgroup = new Checkgroup(trigger)
        checkgroup.setBehavior()
      })
  }
}

export default BRCheckbox
