class BRAccordion {
  constructor(name, component) {
    this.name = name
    this.component = component
    this._setBehavior()
  }

  _setBehavior() {
    for (const button of this.component.querySelectorAll('button.header')) {
      button.addEventListener('click', (event) => {
        this._collapse(event)
        this._changeIcon(event)
      })
    }
  }

  // eslint-disable-next-line complexity
  _collapse(event) {
    if (this.component.hasAttribute('single')) {
      for (const field of this.component.querySelectorAll('.item')) {
        if (field === event.currentTarget.parentNode) {
          if (field.hasAttribute('active')) {
            field.removeAttribute('active')
          } else {
            field.setAttribute('active', '')
          }
        } else {
          if (field.hasAttribute('active')) {
            field.removeAttribute('active')
          }
        }
      }
    } else {
      for (const field of this.component.querySelectorAll('.item')) {
        if (field === event.currentTarget.parentNode) {
          if (field.hasAttribute('active')) {
            field.removeAttribute('active')
          } else {
            field.setAttribute('active', '')
          }
        }
      }
    }
  }

  _changeIcon() {
    for (const field of this.component.querySelectorAll('.item')) {
      if (field.hasAttribute('active')) {
        for (const icon of field.querySelectorAll('.icon')) {
          icon.children[0].classList.remove('fa-angle-down')
          icon.children[0].classList.add('fa-angle-up')
        }
      } else {
        for (const icon of field.querySelectorAll('.icon')) {
          icon.children[0].classList.remove('fa-angle-up')
          icon.children[0].classList.add('fa-angle-down')
        }
      }
    }
  }
}

export default BRAccordion
