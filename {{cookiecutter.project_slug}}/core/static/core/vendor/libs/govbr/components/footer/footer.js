/**
 * Classe do componente BRFooter
 */
class BRFooter {
  /**
   * Instancia um componente BRFooter
   * @param {string} name - Nome do componente (br-footer)
   * @param {object} component - Objeto que referencia o elemento DOM do componente
   */
  constructor(name, component) {
    this.name = name
    this.component = component
    this._setUp()
    this._setBehavior()
  }

  /**
   * Controla a configuração inicial do footer
   */
  _setUp() {
    this.list = this.component.querySelector('.br-list.horizontal')
  }

  /**
   * Controla os comportamentos do footer
   * @private
   */
  _setBehavior() {
    this._setCollapseBehavior()

    window.onresize = function () {
      if (window.matchMedia('(min-width: 992px)').matches) {
        window.document
          .querySelectorAll('.br-footer .br-list:not(.horizontal)')
          .forEach((trigger) => {
            trigger.style.display = 'block'
          })
      } else {
        window.document
          .querySelectorAll('.br-footer .br-list:not(.horizontal)')
          .forEach((trigger) => {
            trigger.style.display = 'none'
          })

        window.document
          .querySelectorAll('.br-footer i')
          .forEach((iconComponent) => {
            iconComponent.classList.remove('fa-angle-up')
            iconComponent.classList.add('fa-angle-down')
          })
      }
    }
  }

  /**
   * Trata do comportamento de collapse do Footer
   * @private
   */
  _setCollapseBehavior() {
    this.britems = []
    if (this.list) {
      this.list.querySelectorAll('.br-list').forEach((trigger) => {
        if (window.matchMedia('(max-width: 992px)').matches) {
          trigger.style.display = 'none'
        }
      })

      this.list.querySelectorAll('.br-item').forEach((trigger) => {
        trigger.addEventListener('click', (e) => {
          if (window.matchMedia('(max-width: 992px)').matches) {
            this._showList(e)
          }
        })
        this.britems.push(trigger)
      })
    }
  }

  /**
   * Controla a abertura e fachamento da lista
   * @param {object} e - Objeto Event
   * @private
   */
  _showList(e) {
    parent = e.target.parentElement

    parent = parent.classList.contains('col-2')
      ? e.target.parentElement
      : e.target.parentElement.parentElement
    parent = parent.classList.contains('col-2')
      ? parent
      : e.target.parentElement.parentElement.parentElement
    // debugger
    this._closeAllColumns(parent)

    parent.querySelectorAll('.br-list ').forEach((trigger) => {
      trigger.style.display =
        trigger.style.display === 'block' ? 'none' : 'block'

      const iconComponent = parent.querySelector('i')

      trigger.style.display === 'block'
        ? this._iconAngleUP(iconComponent)
        : this._iconAngleDOWN(iconComponent)
    })
  }

  /**
   * Fecha todas colunas do Footer
   */
  _closeAllColumns(target) {
    this.component
      .querySelectorAll('.br-list:not(.horizontal)')
      .forEach((trigger) => {
        if (target !== trigger.parentElement) {
          trigger.style.display = 'none'
          this.component
            .querySelectorAll('.header i')
            .forEach((iconComponent) => {
              this._iconAngleDOWN(iconComponent)
            })
        }
      })
  }

  /**
   *Inclui ícone 'fa-angle-up'
   * @param {objetc} iconComponent - Elemento DOM que representa um ícone
   * @private
   */
  _iconAngleUP(iconComponent) {
    iconComponent.classList.remove('fa-angle-down')
    iconComponent.classList.add('fa-angle-up')
  }

  /**
   * Inclui ícone 'fa-angle-down'
   * @param {object} iconComponent - Elemento DOM que representa um ícone
   * @private
   */
  _iconAngleDOWN(iconComponent) {
    iconComponent.classList.remove('fa-angle-up')
    iconComponent.classList.add('fa-angle-down')
  }
}

export default BRFooter
