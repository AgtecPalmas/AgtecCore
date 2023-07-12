/** Classe para instanciar um objeto BRItem*/

class BRItem {
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
    this._setCheckboxSelection()
    this._setRadioSelection()
  }

  /**
   * Define comportamentos do checkbox
   * @private
   */
  _setCheckboxSelection() {
    for (const checkbox of this.component.querySelectorAll(
      '.br-checkbox input[type="checkbox"]'
    )) {
      if (checkbox.checked) {
        this.component.classList.add('selected')
      }
      checkbox.addEventListener('click', (event) => {
        if (event.currentTarget.checked) {
          this.component.classList.add('selected')
        } else {
          this.component.classList.remove('selected')
        }
      })
    }
  }

  /**
   * Define comportamentos do radio
   * @private
   */
  _setRadioSelection() {
    for (const radio of this.component.querySelectorAll(
      '.br-radio input[type="radio"]'
    )) {
      if (radio.checked) {
        radio.setAttribute('checked', '')
        this.component.classList.add('selected')
      }
      radio.addEventListener('click', (event) => {
        for (const item of this.component.parentElement.querySelectorAll(
          '.br-item'
        )) {
          for (const radioItem of item.querySelectorAll(
            '.br-radio input[type="radio"]'
          )) {
            if (radioItem === event.currentTarget) {
              radioItem.setAttribute('checked', '')
              item.classList.add('selected')
            } else {
              radioItem.removeAttribute('checked')
              item.classList.remove('selected')
            }
          }
        }
      })
    }
  }
}

export default BRItem
