class BRScrim {
  constructor(name, component) {
    this.name = name
    this.component = component
    this._setType()
    this._setBehavior()
  }

  _setType() {
    if (this.component.classList.contains('foco')) {
      this._type = 'foco'
    }
    if (this.component.classList.contains('legibilidade')) {
      this._type = 'legibilidade'
    }
    if (this.component.classList.contains('inibicao')) {
      this._type = 'inibicao'
    }
  }

  _setBehavior() {
    if (this.component.classList.contains('foco')) {
      this.component.addEventListener('click', (event) => {
        this.outsideclick = true
        if (event.target.classList.contains('br-scrim')) {
          this.hideScrim(event)
        }
      })

      const allComp = this.component.querySelectorAll(
        `[data-dismiss=${this.component.id}]`
      )

      for (const buttonComponent of allComp) {
        buttonComponent.addEventListener('click', () => {
          this.component.classList.remove('active')
        })
      }
    }
  }

  hideScrim(event) {
    event.currentTarget.classList.remove('active')
  }

  showScrim() {
    if (this._type === 'foco') {
      this.component.classList.add('active')
    }
  }
}
// const scrimList = []
export default BRScrim
for (const buttonBloco1 of window.document.querySelectorAll(
  '.scrimexemplo button'
)) {
  buttonBloco1.addEventListener('click', () => {
    const scrscrim = window.document.querySelector('#scrimexample')
    const scrimfoco = new BRScrim('br-scrim', scrscrim)
    scrimfoco.showScrim()
  })
}
/**
 * Exemplo de scrim com muito texto
 */
for (const scrimexamplebig of window.document.querySelectorAll(
  '#scrimexemplo-big'
)) {
  scrimexamplebig.addEventListener('click', () => {
    const scrscrim = window.document.querySelector('#scrimfocobig')
    const scrimfoco = new BRScrim('br-scrim', scrscrim)
    scrimfoco.showScrim()
  })
}

//Exemplo de scrim close
