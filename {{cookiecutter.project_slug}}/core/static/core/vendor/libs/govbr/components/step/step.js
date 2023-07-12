/** Classe para instanciar um objeto BRStep */
class BRStep {
  constructor(name, component) {
    /**
     * Instancia do componente
     * @param {string} name - Nome do componente em minúsculo
     * @param {object} component - Objeto referenciando a raiz do componente DOM
     * @property {number} activeStepNum - Número do palco ativo
     * @property {array} DOMStrings - instancia dos elementos internos do componente
     */
    this.name = name
    this.component = component
    this.activeStepNum = 0
    this.DOMstrings = {
      // stepsBar: this.component.querySelector('.step-progress'),
      stepsBar: this.component,
      stepsBarClass: 'step-progress',
      stepsBtnClass: 'step-progress-btn',
      stepsBtns: this.component.querySelectorAll('.step-progress-btn'),
    }

    /**
     * Remove uma classe css de uma lista de elementos
     * @param {object} elemSet - Lista de elementos
     * @param {string} button - Nome do atributo
     */
    this.removeAttributes = (elemSet, attrName) => {
      elemSet.forEach((elem) => {
        elem.removeAttribute(attrName)
      })
    }

    /**
     * Retorna o nó pai do elemento com o nome da classe específica
     * @param {object} elem - Referência ao elemento
     * @param {string} parentClass - Nome da classe pai
     * @returns {object} Referência ao elemento pai
     */
    this.findParent = (elem, parentClass) => {
      let currentNode = elem
      while (!currentNode.classList.contains(parentClass)) {
        currentNode = currentNode.parentNode
      }
      return currentNode
    }

    /** Retorna o número do passo de referencia
     * @param {object} elem - Referência ao botão de passo
     * @returns {number} Número do passo
     */
    this.getActiveStep = (elem) => {
      return Array.from(this.DOMstrings.stepsBtns).indexOf(elem)
    }

    /** Define o número do passo de referência como ativo
     * @param {number} num - numero do passo de referência
     */
    this.setActiveStep = function (num) {
      this.removeAttributes(this.DOMstrings.stepsBtns, 'active')
      this.DOMstrings.stepsBtns.forEach((elem, index) => {
        if (index === num) {
          elem.removeAttribute('disabled')
          elem.setAttribute('active', '')
        }
      })
      this.activeStepNum = num
    }

    /**
     * Mostra os números dos rótulos dos passos
     */
    this.setStepsNum = () => {
      this.DOMstrings.stepsBtns.forEach((elem, index) => {
        const img = elem.querySelector('.step-icon')
        const text = this.component.getAttribute('data-type') === 'text'
        if (text) {
          elem.setAttribute(
            'step-num',
            `${index + 1}/${this.DOMstrings.stepsBtns.length}`
          )
        } else if (img) {
          elem.setAttribute('step-num', '')
        } else elem.setAttribute('step-num', index + 1)
      })
    }

    /** Testa se o passo está dentro do escopo e o define como ativo
     * @param {number} num - step number
     */
    this.setStep = (num) => {
      const activeStep = num <= this.DOMstrings.stepsBtns.length ? num - 1 : 0
      this.setActiveStep(activeStep)
    }

    this._setBehavior()
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehavior() {
    this.DOMstrings.stepsBar.addEventListener('click', (e) => {
      const eventTarget = e.target
      if (!eventTarget.classList.contains(`${this.DOMstrings.stepsBtnClass}`)) {
        e.target.parentNode.click()
        return
      }
      const activeStepNum = this.getActiveStep(eventTarget)
      this.setActiveStep(activeStepNum)
    })

    this.setStepsNum()
    if (this.component.hasAttribute('data-initial')) {
      this.setStep(this.component.getAttribute('data-initial'))
    } else this.setStep(1)

    if (
      !this.component.classList.contains('vertical') &&
      !this.component.hasAttribute('data-scroll')
    ) {
      // const stepsWidth = Math.round(100 / this.DOMstrings.stepsBtns.length) - 0.5
    }
  }
}

export default BRStep
