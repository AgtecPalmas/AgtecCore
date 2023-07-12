import Collapse from '../../partial/js/behavior/collapse'
/**
 * Classe do componente BRList
 */
class BRList {
  /**
   * Instancia um componente BRList
   * @param {string} name - Nome do componente (br-list)
   * @param {object} component - Objeto que referencia o elemento DOM do componente
   */
  constructor(name, component) {
    this.name = name
    this.component = component
    this._setBehavior()
  }

  /**
   * Controla os comportamentos da list
   * @private
   */
  _setBehavior() {
    this._setCollapseBehavior()
  }

  /**
   * Trata do comportamento de collapse da list
   * @private
   */
  _setCollapseBehavior() {
    // data-toggle="data-toggle"
    // debugger

    // this.component.querySelectorAll('.br-list').forEach((trigger) => {
    //   // trigger.style.display = 'none'
    // })
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
}
export default BRList
