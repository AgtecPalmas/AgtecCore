import Tooltip from '../../partial/js/behavior/tooltip'
/** Classe para instanciar um objeto BRNotification*/
class BRNotification {
  /**
   * Instancia do objeto
   * @param {string} name - Nome do componente em minúsculo
   * @param {object} component - Objeto referenciando a raiz do componente DOM
   */
  constructor(name, component) {
    this.name = name
    this.component = component
    this.menuBtns = component.querySelectorAll('.contextual-btn')
    this.hideEvents = ['mouseleave', 'blur']
    this._setBehavior()
  }

  /**
   * Esconde a notificação relativa a referência
   * @private
   * @property {object} action - Referência ao Objeto que dispara a ação
   */
  _hideNotification(action) {
    const notification = action.parentNode.parentNode
    notification.setAttribute('hidden', '')
  }

  /**
   * Esconde todas as notificações relativa a referência
   * @private
   * @property {object} action - Referência ao Objeto que dispara a ação
   */
  _hideAllNotifications(action) {
    const notifications =
      action.parentNode.parentNode.parentNode.querySelectorAll('.br-item')
    notifications.forEach((notification) => {
      notification.setAttribute('hidden', '')
    })
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehavior() {
    for (const button of this.component.querySelectorAll(
      '.br-notification .close'
    )) {
      button.addEventListener('click', () => {
        this._dismiss(this.component)
      })
    }
    this._notificationTooltip()
  }

  /**
   * Define tooltip para a notificação
   * @private
   */
  _notificationTooltip() {
    const TooltipExampleList = []

    window.document
      .querySelectorAll(':not(.br-header) .notification-tooltip')
      .forEach((TooltipNotification) => {
        const texttooltip =
          TooltipNotification.getAttribute('data-tooltip-text')
        const config = {
          activator: TooltipNotification,
          placement: 'top',
          textTooltip: texttooltip,
        }
        for (
          parent = TooltipNotification.parentNode;
          parent;
          parent = parent.parentNode
        ) {
          if (parent.classList)
            if (parent.classList.contains('header-avatar')) {
              return ''
            }
        }
        TooltipExampleList.push(new Tooltip(config))
        return ''
      })
  }

  /**
   * Adiciona classe para refletir comportamento de fechar
   * @private
   * @property {object} componente - Referência ao Objeto
   */
  _dismiss(component) {
    component.classList.add('close')
  }
}

export default BRNotification
