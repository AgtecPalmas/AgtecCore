/**
 * Comportamento do grupo de checkboxes
 *
 * Cada checkbox parent em uma cadeia de checkbox terá um objeto próprio para tratar
 * o seu comportamento e de seus filhos. Os eventListeners são declarados em cada objeto,
 * de modo que a execução passa por objetos diferentes quando um checkbox é pai e filho ao mesmo tempo
 *
 * O comportamento é uma sincronia entre os eventos e o objeto que executa o evento
 */
export default class Checkgroup {
  /**
   * Instancia um comportamento de grupo de checkbox
   * @param {object} trigger - Elemento DOM que representa o checkbox acionador do comportamento
   */
  constructor(trigger) {
    this.parent = trigger
    // this.checkedLabel = trigger.dataset.checkedLabel
    // this.uncheckedLabel = trigger.dataset.uncheckedLabel
    this.children = this._setChildren(trigger.dataset.parent)
  }

  /**
   * Pega dinamincamente o valor do atributo data-checked-label
   * @type {string} - O valor do atributo data-checked-label ou o valor da label, caso não tenha o atributo
   * @readonly
   * @public
   */
  get checkedLabel() {
    return (
      this.parent.dataset.checkedLabel ||
      this.parent.nextElementSibling.innerText
    )
  }

  /**
   * Pega dinamincamente o valor do atributo data-unchecked-label
   * @type {string} - O valor do atributo data-unchecked-label ou o valor da label, caso não tenha o atributo
   * @readonly
   * @public
   */
  get uncheckedLabel() {
    return (
      this.parent.dataset.uncheckedLabel ||
      this.parent.nextElementSibling.innerText
    )
  }

  /**
   * Configurar o comportamento do grupo de checkbox
   * @public
   */
  setBehavior() {
    this._setParentBehavior()
    this._setChildBehavior()
  }

  /**
   * Obtem todos os checkboxes filhos do checkbox pai
   * @param {string} tag - Nome que indica a relação entre checkbox pai e checkbox filho
   * @returns {array} - Array contendo os elementos DOM que representam os checkboxes filhos.
   */
  _setChildren(tag) {
    return document.querySelectorAll(`[data-child="${tag}"]`)
  }

  /**
   * Trata do comportamento do checkbox pai
   * @private
   */
  _setParentBehavior() {
    this.parent.addEventListener('click', this._handleParentClick.bind(this))
    this.parent.addEventListener('change', this._handleParentChange.bind(this))
  }

  /**
   * Handler que trata o evento click no parent
   * @private
   */
  _handleParentClick() {
    if (!this.parent.hasAttribute('data-parent-sync')) {
      this._setIndeterminateStateOnClick()
    }
    this._setParentCheckboxLabel()
  }

  /**
   * Trata o estado indeterminado no evento click da etapa de interação do usuário
   * @private
   */
  _setIndeterminateStateOnClick() {
    if (this.parent.hasAttribute('indeterminate')) {
      this.parent.removeAttribute('indeterminate')
      this.parent.checked = true
    }
  }

  /**
   * Handler que trata o evento change no parent
   * @private
   */
  _handleParentChange() {
    if (!this.parent.hasAttribute('data-parent-sync')) {
      this._changeChildState()
      this._setParentCheckboxLabel()
    } else {
      this.parent.removeAttribute('data-parent-sync')
    }
  }

  /**
   * Trata do estado do checkboxes filhos
   * @private
   */
  _changeChildState() {
    this.children.forEach((child) => {
      if (
        child.checked !== this.parent.checked ||
        child.hasAttribute('indeterminate')
      ) {
        child.removeAttribute('indeterminate')
        child.checked = this.parent.checked
        child.dispatchEvent(new Event('change'))
      }
    })
  }

  /**
   * Trata do comportamento dos checkboxes filhos
   * @private
   */
  _setChildBehavior() {
    this.children.forEach((child) => {
      child.addEventListener('click', this._handleChildClick.bind(this))
      child.addEventListener('change', this._handleChildChange.bind(this))
    })
  }

  /**
   * Handler que trata do evento click no filho
   * @param {object} event - Objeto Event
   * @private
   */
  _handleChildClick(event) {
    event.currentTarget.setAttribute('data-child-sync', '')
  }

  /**
   * Handler que trata do evento change no filho
   * @param {object} event - Objeto Event
   * @private
   */
  _handleChildChange(event) {
    if (event.currentTarget.hasAttribute('data-child-sync')) {
      this._setIndeterminateStateOnChildChange()
      this.parent.setAttribute('data-parent-sync', '')
      this.parent.dispatchEvent(new Event('click'))
      this.parent.dispatchEvent(new Event('change'))
      event.currentTarget.removeAttribute('data-child-sync')
    }
  }

  /**
   * Trata o estado indeterminado no evento click da etapa de sincronia
   * @private
   */
  _setIndeterminateStateOnChildChange() {
    if (this._isAllChildrenChecked()) {
      this.parent.removeAttribute('indeterminate')
      this.parent.checked = true
    } else if (this._isAllChildrenUnchecked()) {
      this.parent.removeAttribute('indeterminate')
      this.parent.checked = false
    } else {
      this.parent.setAttribute('indeterminate', '')
      this.parent.checked = true
    }
  }

  /**
   * Verifica se todos os checkboxes filhos estão selecionados
   * @returns {boolean} - true se todos os checkboxes filhos estão selecionados
   *                      false se pelo menos 1 checkbox filho não está selecionado
   * @private
   */
  _isAllChildrenChecked() {
    let allChildChecked = true
    this.children.forEach((child) => {
      if (!child.checked || child.hasAttribute('indeterminate')) {
        allChildChecked = false
      }
    })
    return allChildChecked
  }

  /**
   * Verifica se todos so checkboxes filhos estão desselecionados
   * @returns {boolean} - true se todos os checkboxes filhos estão desselecionados
   *                      false se pelo menos 1 checkbox filho está selecionado
   * @private
   */
  _isAllChildrenUnchecked() {
    let allChildUnchecked = true
    this.children.forEach((child) => {
      if (child.checked) {
        allChildUnchecked = false
      }
    })
    return allChildUnchecked
  }

  /**
   * Configura a label do checkbox pai
   * @private
   */
  _setParentCheckboxLabel() {
    if (this.parent.checked && !this.parent.hasAttribute('indeterminate')) {
      this.parent.nextElementSibling.innerHTML = this.uncheckedLabel
      this.parent.setAttribute('aria-label', this.uncheckedLabel)
    } else {
      this.parent.nextElementSibling.innerHTML = this.checkedLabel
      this.parent.setAttribute('aria-label', this.checkedLabel)
    }
  }
}
