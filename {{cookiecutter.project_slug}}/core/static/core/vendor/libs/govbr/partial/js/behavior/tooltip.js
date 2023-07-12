import { createPopper } from '@popperjs/core'
// import 'tippy.js/dist/tippy.css' // optional for styling
class Tooltip {
  /**
   * Instancia um comportamento Tooltip
   * @param {object} - Objeto de configuração inicial para tooltip
   * @property {object} component - Elemento DOM do tooltip (opcional se tiver o textTooltip)
   * @property {object} activator - Elemento DOM que representa o acionador do comportmento tooltip
   * @property {string} place -Local onde vai aparecer o tooltip ('top', 'right', 'bottom', 'left')
   * @property {string} timer - Tempo em que vai aparecer o tooltip em milisegunto (opcional)
   * @property {string} textTooltip - Texto que vai ser mostrado quando não estiver instaciado o atributo component
   * @property {string} type - Tipo de tooltip (info, warning) padrão info
   * @property {boolean} onActivator - Adiciona o tooltip dentro do elemento ativador padrão false
   */
  
  constructor({
    component,
    activator,
    place = 'top',
    timer,
    active,
    textTooltip,
    type = 'info',
    onActivator = false
  }) {
    
    const text_tooltip = textTooltip ? textTooltip : component
    this.onActivator = onActivator 
    this.activator = activator
    this.component = component
      ? component
      : this._setContent(text_tooltip, type)

    this.place =
      this.component.getAttribute('place') === null
        ? this.component.getAttribute('place')
        : place
    const positions = ['top', 'right', 'bottom', 'left']
    this.popover = this.component.hasAttribute('popover')
    this.notification = this.component.classList.contains('br-notification')
    this.timer = this.component.getAttribute('timer')
      ? this.component.getAttribute('timer')
      : timer
    this.active = this.component.hasAttribute('active')
      ? this.component.hasAttribute('active')
      : active
    this.placement = positions.includes(place)
      ? place
      : this.notification

      
    this.popperInstance = null
    this.showEvents = ['mouseenter', 'click', 'focus']
    this.hideEvents = ['mouseleave', 'blur']
    this.closeTimer = null
    this._create()
    this._setBehavior()
  }
  /**
   * Instancializa o behavior
   */
  _setBehavior() {
    // Ação de abrir padrao ao entrar no ativador
    if (this.activator) {
      this.showEvents.forEach((event) => {
        this.activator.addEventListener(event, (otherEvent) => {
          this._show(otherEvent)
        })
      })
    }
    // Adiciona ação de fechar ao botao do popover
    
    if (this.popover) {
      const closeBtn = this.component.querySelector('.close')
      closeBtn.addEventListener('click', (event) => {
        this._hide(event, this.component)
        this._toggleActivatorIcon()
      })
      // Ação de fechar padrao ao sair do ativador
    } else {
      this.hideEvents.forEach((event) => {
        this.activator.addEventListener(event, (otherEvent) => {
          this._hide(otherEvent, this.component)
        })
      })
    }
  }
  /**
   * Inclui o conteudo do tooltip
   * @param {*} contentText conteudo do texto do tooltip
   * @param {*} type tipo de tooltip
   * @returns  - retorna o objeto com tooltip
   */
  _setContent(contentText, type) {
    const text_tooltip = document.createElement('div')
    text_tooltip.setAttribute('role', 'tooltip')
    text_tooltip.setAttribute('place', 'top')
    text_tooltip.setAttribute(type, type)
    text_tooltip.innerText = `${contentText}`
    text_tooltip.classList.add('br-tooltip')
    //TODO: Retirar sample que utiliza não conflita com tooltip componente que está sendo depreciado
    text_tooltip.classList.add('sample')
    if (this.activator && this.onActivator) {
      this.activator.appendChild(text_tooltip)
    }else{
      document.body.appendChild(text_tooltip)
    }

    return text_tooltip
  }

  /**
   * Cria a instancia do popper
   * @private
   */

  _create() {
    this._setLayout()

    if (this.notification) {
      this.component.setAttribute('notification', '')
      this.popperInstance = createPopper(this.activator, this.component, {
        modifiers: [
          {
            name: 'offset',
            options: {
              offset: [0, 8],
            },
          },
          {
            name: 'preventOverflow',
            options: {
              altAxis: false, // false by default
              mainAxis: true, // true by default
              
            },
          },
          {name: 'flip',options: {fallbackPlacements: ['top', 'right'],},},
        ],
        // placement: this.placement,
        placement: 'bottom',
        strategy: 'fixed',
      })
    } else {
      
    
      
      this.popperInstance = createPopper(this.activator, this.component, {
        modifiers: [
          {
            name: 'offset',
            options: {
              offset: [0, 8],
            },
          },
          {
            name: 'preventOverflow',
            options: {
              altAxis: true, 
              mainAxis: true, 
              
              
            },
          },
          {name: 'flip',options: {fallbackPlacements: ['top', 'right',"bottom","left"],},},
        ],
        placement: this.placement,
      })
    }
  }
  /**
   * Mostra o tooltip e define o timeout se tiver
   * @param {object} event  evento javascript
   */
  _show(event) {
    
    this.component.style.display = 'unset'
    this.component.setAttribute('data-show', '')
    this.component.style.zIndex = 9999
    this.popperInstance.update()
    // Importante pois "display: none" conflitua com a instancia do componente e precisa ser setado aqui já que pelo css ativa o efeito fade no primeiro carregamento
    this.component.style.visibility = 'visible'
    if (this.timer) {
      console.log("timer",this.timer)
      clearTimeout(this.closeTimer)
      this.closeTimer = setTimeout(
        this._hide,
        this.timer,
        event,
        this.component
      )
    }
  }

  

  /**
   * Esconde o componente
   * @private
   */
  _hide(event, component) {
    component.removeAttribute('data-show')
    component.style.zIndex = -1
    component.style.visibility = 'hidden'
    clearTimeout(component.closeTimer)
  }
  /**
   * Cria o laytout do tooltip
   * @private
   */
  _setLayout() {
    // Cria a setinha que aponta para o item que criou o tooltip
    const arrow = document.createElement('div')
    arrow.setAttribute('data-popper-arrow', '')

    if (this.component.querySelectorAll('.arrow').length < 1) {
      arrow.classList.add('arrow')
    }
    this.component.appendChild(arrow)
    // Cria o icone de fechar do po over
    if (this.popover) {
      const close = document.createElement('button')
      close.setAttribute('type', 'button')
      close.classList.add('close')
      const ico = document.createElement('i')
      ico.classList.add('fas', 'fa-times')
      close.appendChild(ico)
      this.component.appendChild(close)
    }
  }
  /**
   * Muda icone da seta
   * @private
   */
  _toggleActivatorIcon() {
    const icon = this.activator.querySelector('button svg')
    if (icon) {
      icon.classList.toggle('fa-angle-down')
      icon.classList.toggle('fa-angle-up')
    }
    this.activator.toggleAttribute('active')
  }
  
  
}

export default Tooltip

