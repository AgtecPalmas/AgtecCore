import Dropdown from '../../partial/js/behavior/dropdown'

/**
 * Classe para o exemplo do comportamento dropdown
 */
class BRAvatar {
  /**
   * Instancia um exemplo de comportamento dropdown
   * @param {string} name - Nome do componente
   * @param {object} component - Referência ao objeto do DOM
   */
  constructor(name, component) {
    this.name = name
    this.component = component
    this._setBehavior()
  }

  /**
   * Define os comportamentos do componente
   * @private
   */
  _setBehavior() {
    this._setDropdownBehavior()
  }

  /**
   * Define os comportamentos do dropdown
   * @private
   */
  _setDropdownBehavior() {
    if (this.component.parentElement.dataset.toggle === 'dropdown') {
      const config = {
        iconToHide: 'fa-caret-up',
        iconToShow: 'fa-caret-down',
        trigger: this.component.parentElement,
        useIcons: true,
      }
      const dropdown = new Dropdown(config)
      dropdown.setBehavior()
    }
  }
}

export default BRAvatar
