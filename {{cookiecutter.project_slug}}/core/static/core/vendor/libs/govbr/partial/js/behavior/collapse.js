/** Classe para o comportamento Collapse */
export default class Collapse {
  /**
   * Instancia um comportamento collapse
   * @param {object} - Objeto de configuração inicial para destructuring
   * @property {object} trigger - Elemento DOM que representa o acionador do comportmento collapse
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
    this.trigger = trigger
    this.useIcons = useIcons
    this.breakpoint = trigger.getAttribute('data-breakpoint')
    this.setIconToShow(iconToShow)
    this.setIconToHide(iconToHide)
    this._setTarget()
    this._setUp()
  }

  /**
   * Determina qual elemento DOM é o alvo do comportamento collapse
   * @private
   */
  _setTarget() {
    this.target = document.querySelector(
      `#${this.trigger.getAttribute('data-target')}`
    )
  }

  // TODO: Melhorar a solução
  _checkBreakpoint() {
    if (this.breakpoint) {
      if (window.matchMedia('(min-width: 977px)').matches) {
        this.target.removeAttribute('hidden')
      }
    }
  }

  /**
   * Trata a configuração inicial do comportamento collapse
   * @private
   */
  _setUp() {
    this._setVisibilityStatus()
    if (this.useIcons) {
      this._toggleIcon()
    }
    this.trigger.setAttribute(
      'aria-controls',
      `${this.trigger.getAttribute('data-target')}`
    )
    this._checkBreakpoint()
  }

  /**
   * Configura o estado de visualização do comportamento collapse
   * @private
   */
  _setVisibilityStatus() {
    this._setTriggerVisibilityStatus()
    this._setTargetVisibilityStatus()
  }

  /**
   * Trata o estado de visualização do acionador
   * @private
   */
  _setTriggerVisibilityStatus() {
    if (this.target) {
      if (this.target.hasAttribute('hidden')) {
        this.trigger.setAttribute('data-visible', false)
        this.trigger.setAttribute('aria-expanded', false)
      } else {
        this.trigger.setAttribute('data-visible', true)
        this.trigger.setAttribute('aria-expanded', true)
      }
    }
  }

  /**
   * Trata o estado de visualização do alvo
   * @private
   */
  _setTargetVisibilityStatus() {
    if (this.target) {
      if (this.target.hasAttribute('hidden')) {
        this.target.setAttribute('aria-hidden', true)
      } else {
        this.target.setAttribute('aria-hidden', false)
      }
    }
  }

  /**
   * Handler para o evento de click no acionador do comportamento collapse
   * Lança um evento 'change' a cada troca
   * @private
   */
  _handleTriggerClickBehavior() {
    if (this.breakpoint) {
      if (window.matchMedia('(max-width: 977px)').matches) {
        this._toggleVisibility()
        if (this.useIcons) {
          this._toggleIcon()
        }
        this.trigger.dispatchEvent(new Event('change'))
      }
    } else {
      this._toggleVisibility()
      if (this.useIcons) {
        this._toggleIcon()
      }
      this.trigger.dispatchEvent(new Event('change'))
    }
  }

  /**
   * Alterna o estado de visualização do comportamento collapse
   * @private
   */
  _toggleVisibility() {
    if (this.target) {
      this.target.hasAttribute('hidden')
        ? this.target.removeAttribute('hidden')
        : this.target.setAttribute('hidden', '')

      this._setVisibilityStatus()
    }
  }

  /**
   * Troca o icone do acionador após uma mudança no estado de visualização do alvo
   * Para o estado 'hidden' usa o iconToShow e para o estado 'shown' usa o iconToHide
   * @public
   */
  _toggleIcon() {
    this.trigger.querySelectorAll('i.fas').forEach((icon) => {
      if (this.target) {
        icon.classList.remove(
          this.target.hasAttribute('hidden') ? this.iconToHide : this.iconToShow
        )
        icon.classList.add(
          this.target.hasAttribute('hidden') ? this.iconToShow : this.iconToHide
        )
      }
    })
  }

  /**
   * Configura o comportamento collapse
   * @public
   */
  setBehavior() {
    this.trigger.addEventListener(
      'click',
      this._handleTriggerClickBehavior.bind(this)
    )
  }

  /**
   * Determina a classe do icone para mostrar o conteúdo
   * @param {string} iconToShow - Classe que representa o ícone para mostrar o conteúdo
   * @public
   */
  setIconToShow(iconToShow) {
    this.iconToShow = iconToShow
  }

  /**
   * Determina a classe do ícone para esconder o conteúdo
   * @param {string} iconToHide - Classe que representa o ícone para esconder o conteúdo
   * @public
   */
  setIconToHide(iconToHide) {
    this.iconToHide = iconToHide
  }
}
