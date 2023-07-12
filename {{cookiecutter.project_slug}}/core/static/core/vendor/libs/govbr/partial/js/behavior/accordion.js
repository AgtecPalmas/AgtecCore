import Collapse from './collapse'

/**
 * Classe para o comportamento Accordion.
 * O Comportamento Accordion é um agrupador de comportamentos Collapse
 */
export default class Accordion extends Collapse {
  /**
   * Instancia um comportamento accordion
   * @param {object} - Objeto de configuração inicial para destructuring
   * @property {object} trigger - Elemento DOM que representa o acionador do comportmento accordion
   * @property {string} iconToShow - Classe que representa o ícone para mostrar o conteúdo (padrão: fa-chevron-down)
   * @property {string} iconToHide - Classe que representa o ícone para esconder o conteúdo (padrão: fa-chevron-up)
   * @property {boolean} useIcons - true: com ícone | false: sem ícone (padrão: true)
   */
  constructor({
    trigger,
    iconToShow = 'fa-chevron-down',
    iconToHide = 'fa-chevron-up',
    useIcons = true,
  }) {
    super({ iconToHide, iconToShow, trigger, useIcons })
    this._setUp()
  }

  /**
   * Trata a configuração inicial do comportamento accordion
   * @private
   */
  _setUp() {
    super._setUp()
    this._setPriorityVisibility()
  }

  /**
   * Determina qual acionador vai estar visivel, caso mais de 1 acionador esteja visivel no grupo.
   * Prioridade de cima para baixo
   * @private
   */
  _setPriorityVisibility() {
    for (let i = 0; i < this._getGroup().length; i += 1) {
      if (this._getGroup()[i].dataset.visible === 'true') {
        this._synchronizeAccordion(this._getGroup()[i])
        break
      }
    }
  }

  /**
   * Obtém todos os acionadores pertencentes ao grupo do comportamento accordion
   * @returns {array} - Conjunto de elementos DOM representando os acionadores pertencentes ao grupo do comportamento accordion
   * @private
   */
  _getGroup() {
    return document.querySelectorAll(
      `[data-group="${this.trigger.getAttribute('data-group')}"]`
    )
  }

  /**
   * Handler para o evento 'change' do acionador
   * @param {object} event - Objeto do tipo Event
   * @private
   */
  _handleTriggerChangeBehavior(event) {
    if (!event.currentTarget.hasAttribute('data-sync')) {
      this._synchronizeAccordion(event.currentTarget)
    } else {
      event.currentTarget.removeAttribute('data-sync')
    }
  }

  /**
   * Sincroniza o grupo de accordion mostrando 1 elemento aberto por vez
   * @param {object} currentTrigger - Elemento DOM representando um acionador do comportamento accordion
   * @private
   */
  _synchronizeAccordion(currentTrigger) {
    this._getGroup().forEach((trigger) => {
      if (trigger !== currentTrigger && trigger.dataset.visible === 'true') {
        trigger.setAttribute('data-sync', '')
        trigger.click()
      }
    })
  }

  /**
   * Configura o comportamento accordion
   * @public
   */
  setBehavior() {
    super.setBehavior()
    this.trigger.addEventListener(
      'change',
      this._handleTriggerChangeBehavior.bind(this)
    )
  }
}
