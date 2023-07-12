import Swipe from '../../partial/js/behavior/swipe'

/** Classe para instanciar um objeto BRWizard*/
class BRWizard {
  /**
   * Instância do componente
   * @param {string} name - nome do componente
   * @param {object} component - referencia ao objeto do DOM
   **/
  constructor(name, component) {
    this.name = name
    this.component = component
    this.DOMstrings = {
      stepFormPanelClass: 'wizard-panel',
      stepFormPanels: this.component.querySelectorAll('.wizard-panel'),
      stepNextBtnClass: 'wizard-btn-next',
      stepPrevBtnClass: 'wizard-btn-prev',
      stepsBar: this.component.querySelector('.wizard-progress'),
      stepsBarClass: 'wizard-progress',
      stepsBtnClass: 'wizard-progress-btn',
      stepsBtns: this.component.querySelectorAll('.wizard-progress-btn'),
      stepsForm: this.component.querySelector('.wizard-form'),
    }
    /**
     * Retira o atributo de uma lista de elementos
     * @param {object[]} elementSet - Lista de objetos
     * @param {string} attrName - Nome do atribbuto
     */
    this.removeAttributes = (elemSet, attrName) => {
      elemSet.forEach((elem) => {
        elem.removeAttribute(attrName)
      })
    }

    /**
     * Retorna o elemento pai do objeto com a classe de referência
     * @param {object} elem - Lista de objetos
     * @param {string} parentClass - nome da classe de referência
     * @returns {object}
     */
    this.findParent = (elem, parentClass) => {
      let currentNode = elem
      while (!currentNode.classList.contains(parentClass)) {
        currentNode = currentNode.parentNode
      }
      return currentNode
    }

    /**
     * Retorna o índice do elemento botão de passo
     * @param {object} elem - botão de passo
     * @returns {number}
     */
    this.getActiveStep = (elem) => {
      return Array.from(this.DOMstrings.stepsBtns).indexOf(elem)
    }

    /**
     * Define o estado do botão ativo e limpa os demais estados dos botões
     * @param {number} activeStepNum - número do botão ativo
     */
    this.setActiveStep = function (activeStepNum) {
      this.removeAttributes(this.DOMstrings.stepsBtns, 'active')
      this.DOMstrings.stepsBtns.forEach((elem, index) => {
        if (index === activeStepNum) {
          elem.removeAttribute('disabled')
          elem.setAttribute('active', '')
        }
      })
    }

    /**
     * Retorna o índice do painel ativo
     * @returns {number}
     */
    this.getActivePanel = () => {
      let activePanel
      this.DOMstrings.stepFormPanels.forEach((elem) => {
        if (elem.hasAttribute('active')) {
          activePanel = elem
        }
      })
      return activePanel
    }

    /**
     * Abre o painel ativo e fecha paineis inativos
     * @param {number} activePanelNum - numero do painel
     */
    this.setActivePanel = (activePanelNum) => {
      // remove active class from all the panels
      this.removeAttributes(this.DOMstrings.stepFormPanels, 'active')
      // show active panel
      this.DOMstrings.stepFormPanels.forEach((elem, index) => {
        if (index === activePanelNum) {
          elem.setAttribute('active', '')
        }
      })
    }

    /**
     * Define números dos passos
     */
    this.setStepsNum = () => {
      this.DOMstrings.stepsBtns.forEach((elem, index) => {
        elem.setAttribute('step', index + 1)
      })
    }

    /**
     * Define passo e painel ativo
     * @param {number} num - numero do passo
     */
    this.setStep = (num) => {
      const activeStep = num <= this.DOMstrings.stepsBtns.length ? num - 1 : 0
      this.setActiveStep(activeStep)
      this.setActivePanel(activeStep)
    }

    /**
     * Retrai painel de passos
     */
    this.collapseSteps = () => {
      this.component.setAttribute('collapsed', '')
    }

    /**
     * Expande painel de passos
     */
    this.expandSteps = () => {
      this.component.removeAttribute('collapsed')
    }

    this._setBehavior()
  }

  /**
   * Define os comportamentos do componente
   * @private
   */
  _setBehavior() {
    /**
     * Mapeia clique na barra de passos
     */
    this.DOMstrings.stepsBar.addEventListener('click', (e) => {
      const eventTarget = e.target
      if (!eventTarget.classList.contains(`${this.DOMstrings.stepsBtnClass}`)) {
        e.target.parentNode.click()
        return
      }
      const activeStep = this.getActiveStep(eventTarget)
      this.setActiveStep(activeStep)
      this.setActivePanel(activeStep)
    })

    /**
     * Mapeia clique nos botões de navegação
     */
    this.DOMstrings.stepsForm.addEventListener('click', (e) => {
      const eventTarget = e.target
      if (
        !(
          eventTarget.classList.contains(
            `${this.DOMstrings.stepPrevBtnClass}`
          ) ||
          eventTarget.classList.contains(`${this.DOMstrings.stepNextBtnClass}`)
        )
      ) {
        return
      }
      const activePanel = this.findParent(
        eventTarget,
        `${this.DOMstrings.stepFormPanelClass}`
      )
      let activePanelNum = Array.from(this.DOMstrings.stepFormPanels).indexOf(
        activePanel
      )
      if (
        eventTarget.classList.contains(`${this.DOMstrings.stepPrevBtnClass}`)
      ) {
        activePanelNum -= 1
        activePanel.style.left = '1%'
      } else {
        activePanelNum += 1
        activePanel.style.left = '-1%'
      }
      this.setActiveStep(activePanelNum)
      this.setActivePanel(activePanelNum)
    })

    this.setStepsNum()

    if (this.component.hasAttribute('step')) {
      this.setStep(this.component.getAttribute('step'))
    }

    if (
      this.component.hasAttribute('scroll') &&
      !this.component.hasAttribute('vertical')
    ) {
      const stepsWidth =
        Math.round(100 / this.DOMstrings.stepsBtns.length) - 0.5
      this.DOMstrings.stepsBar.style.gridTemplateColumns = `repeat(auto-fit, minmax(100px, ${stepsWidth}% ))`
    }

    /**
     * Configura gestos (swipe)
     */
    const dispatcher = new Swipe(this.DOMstrings.stepsBar)
    if (this.component.hasAttribute('vertical')) {
      dispatcher.on('SWIPE_LEFT', () => {
        this.collapseSteps()
      })
      dispatcher.on('SWIPE_RIGHT', () => {
        this.expandSteps()
      })
      this.DOMstrings.stepsForm.ontouchstart = () => {
        this.collapseSteps()
      }
    } else {
      this.DOMstrings.stepsBar.ontouchstart = () => {
        this.expandSteps()
      }
      this.DOMstrings.stepsForm.ontouchstart = () => {
        this.collapseSteps()
      }
    }
  }
}

export default BRWizard
