import { createPopper } from '@popperjs/core'
class BRTooltip {
  constructor(name, component) {
    this.name = name
    this.component = component
    this.activator = component.previousSibling.previousSibling
    const place = component.getAttribute('place')
    const positions = ['top', 'right', 'bottom', 'left']
    this.popover = component.hasAttribute('popover')
    this.notification = component.classList.contains('br-notification')
    this.timer = component.getAttribute('timer')
    let positionNotification = this.notification
    ? 'bottom'
    : 'top'
    this.active = component.hasAttribute('active')
    this.placement = positions.includes(place)
      ? place
      : positionNotification
    this.popperInstance = null
    this.showEvents = ['mouseenter', 'click', 'focus']
    this.hideEvents = ['mouseleave', 'blur']
    this.closeTimer = null

    this._create()
    this._setBehavior()
  }

  _setBehavior() {
    // Ação de abrir padrao ao entrar no ativador

    if (this.activator) {
      this.showEvents.forEach((event) => {
        this.activator.addEventListener(event, (otherEvent) => {
          this._show(otherEvent)
        })
      })
      // }
    }
    // Adiciona ação de fechar ao botao do popover
    // if (this.popover || this.notification) {
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

  _create() {
    this._setLayout()


    // Cria a instancia do popper
    if (this.notification) {
      this.component.setAttribute('notification', '')

      this.popperInstance = createPopper(this.activator, this.component, {
        modifiers: [
          {
            name: 'offset',
            options: {
              offset: [0, 10],
            },
          },
          {
            name: 'preventOverflow',
            options: {
              altAxis: false, 
              mainAxis: true, 
              
            },
          },
        ],
        placement: this.placement,
        
        strategy: 'fixed',
      })
    } else {
      let ac = new DOMRect()
      const tt = new DOMRect()

      
      
      
     
        ac = this.activator.getBoundingClientRect()
      

      const bw = document.body.clientWidth
      if (this.placement === 'right') {
        this.placement =
          ac.x + ac.width + tt.width > bw ? 'top' : this.placement
      }
      if (this.placement === 'left') {
        this.placement = ac.x - tt.width > 0 ? this.placement : 'top'
      }

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
              tether: false, 
            },
          },
        ],
        placement: this.placement,
      })
    }
  }

  _show(event) {
    this.component.style.display = 'unset'
    this.component.setAttribute('data-show', '')
    this.component.style.zIndex = 99
    this._fixPosition()
    
    // Importante pois "display: none" conflitua com a instancia do componente e precisa ser setado aqui já que pelo css ativa o efeito fade no primeiro carregamento

    this.component.style.visibility = 'visible'
    if (this.timer) {
      clearTimeout(this.closeTimer)
      console.log("Timer",this.timer)
      this.closeTimer = setTimeout(
        this._hide,
        this.timer,
        event,
        this.component
      )
    }
  }

  _hide(event, component) {
    component.removeAttribute('data-show')
    component.style.zIndex = -1
    component.style.visibility = 'hidden'
    clearTimeout(component.closeTimer)
  }

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

  _toggleActivatorIcon() {
    const icon = this.activator.querySelector('button svg')
    if (icon) {
      icon.classList.toggle('fa-angle-down')
      icon.classList.toggle('fa-angle-up')
    }
    this.activator.toggleAttribute('active')
  }

  _fixPosition() {
    if (this.notification) {
      setTimeout(() => {
        const ac = this.activator.getBoundingClientRect()
        this.component.style = `position: fixed !important; top: ${
          ac.top + ac.height + 10
        }px !important; left: auto; right: 8px; display: unset; bottom: auto;`
        this.component.querySelector(
          '.arrow'
        ).style = `position: absolute; left: auto; right: ${
          document.body.clientWidth - ac.right + ac.width / 5
        }px !important;`
      }, 10)
    }
  }
}

export default BRTooltip
