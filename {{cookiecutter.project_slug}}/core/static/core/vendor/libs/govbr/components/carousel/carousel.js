import Swipe from '../../partial/js/behavior/swipe'
import BRStep from '../step/step'
class BRCarousel {
  constructor(name, component) {
    /**
     * Instancia um componente carousel
     * @param {string} name - Nome do componente
     * @param {object} component - Objeto referenciando a raiz do componente DOM
     * @property {number} activeStageNum - Número do palco ativo
     * @property {array} DOMStrings - instancia dos elementos internos do componente
     * @property {BRStep} DOMStrings - instancia dos elemento step interno
     */
    this.name = name
    this.component = component
    this.activeStageNum = 0
    // Elementos DOM
    this.DOMstrings = {
      carouselNextBtn: this.component.querySelector('.carousel-btn-next'),
      carouselPages: this.component.querySelectorAll('.carousel-page'),
      carouselPrevBtn: this.component.querySelector('.carousel-btn-prev'),
      carouselStage: this.component.querySelector('.carousel-stage'),
      circular: this.component.hasAttribute('data-circular'),
      step: this.component.querySelector('.br-step'),
    }
    this.step = new BRStep('br-step', this.DOMstrings.step)
    this._setBehavior()
  }

  /**
   * Remove os atributos de uma lista de elementos
   * @param {object} elemSet - Lista de elementos
   * @param {string} button - Nome do atributo
   */
  removeAttributes(elemSet, attrName) {
    elemSet.forEach((elem) => {
      elem.removeAttribute(attrName)
    })
  }

  /**
   * Retorna o passo ativo
   */
  getActiveStep() {
    return this.step.activeStepNum
  }

  /**
   * Define o passo ativo
   * @param {number} activeStepNum - número do passo
   */
  setActiveStep(activeStepNum) {
    this.step.setActiveStep(activeStepNum)
  }

  /**
   * Retorna o palco ativo
   */
  getActiveStage() {
    let activeStage
    this.DOMstrings.carouselPages.forEach((stage) => {
      if (stage.hasAttribute('active')) {
        activeStage = stage
      }
    })
    return activeStage
  }

  /**
   * Define o palco ativo
   * @param {number} num - número do palco
   */
  setActiveStage(num) {
    // remove active atts from all the stages
    this.removeAttributes(this.DOMstrings.carouselPages, 'active')
    // show active stage
    this.DOMstrings.carouselPages.forEach((stage, index) => {
      // motion efect
      if (index > num) {
        stage.style.left = '100%'
      } else {
        stage.style.left = '-100%'
      }
      // set active attrb
      if (index === num) {
        stage.setAttribute('active', '')
        this.activeStageNum = num
      }
    })
    this.disabledBtns()
  }

  /**
   * Desabilita os botões se o carousel não for circular
   */
  disabledBtns() {
    // Disables Carousel Buttons
    if (!this.DOMstrings.circular) {
      if (this.activeStageNum === 0) {
        this.DOMstrings.carouselPrevBtn.setAttribute('disabled', '')
      } else {
        this.DOMstrings.carouselPrevBtn.removeAttribute('disabled')
      }
      if (this.activeStageNum === this.DOMstrings.carouselPages.length - 1) {
        this.DOMstrings.carouselNextBtn.setAttribute('disabled', '')
      } else {
        this.DOMstrings.carouselNextBtn.removeAttribute('disabled')
      }
    }
  }

  /**
   * Muda a página ativa incrementalmente - ações de botões e swap
   * @param {number} num - incremento
   */
  shiftPage(num) {
    //find active stage
    const activeStage = this.getActiveStage()
    const PanelsSize = this.DOMstrings.carouselPages.length - 1
    let activeStageNum = Array.from(this.DOMstrings.carouselPages).indexOf(
      activeStage
    )
    // set active step and active stage onclick
    if (num < 0) {
      // Volta o slide
      if (this.DOMstrings.circular) {
        activeStageNum =
          activeStageNum === 0 ? PanelsSize : (activeStageNum -= 1)
      } else {
        activeStageNum -= activeStageNum === 0 ? 0 : 1
      }
    } else {
      // Passar p/ frente o slide
      if (this.DOMstrings.circular) {
        activeStageNum =
          activeStageNum === PanelsSize ? 0 : (activeStageNum += 1)
      } else {
        activeStageNum += activeStageNum === PanelsSize ? 0 : 1
      }
    }
    this.setActiveStep(activeStageNum)
    this.setActiveStage(activeStageNum)
  }

  /**
   * Define os comportamentos do componente
   * @private
   */
  _setBehavior() {
    this.DOMstrings.carouselNextBtn.addEventListener('click', () => {
      this.shiftPage(1)
    })

    this.DOMstrings.carouselPrevBtn.addEventListener('click', () => {
      this.shiftPage(-1)
    })

    this.DOMstrings.step.addEventListener('click', () => {
      this.setActiveStage(this.step.activeStepNum)
    })

    // Swipe
    const dispatcher = new Swipe(this.DOMstrings.carouselStage)
    dispatcher.on('SWIPE_LEFT', () => {
      this.shiftPage(1)
    })
    dispatcher.on('SWIPE_RIGHT', () => {
      this.shiftPage(-1)
    })
    this.disabledBtns()
  }
}

export default BRCarousel
