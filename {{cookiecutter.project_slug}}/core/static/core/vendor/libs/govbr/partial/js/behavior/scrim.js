/** Classe para o comportamento scrim */
export default class Scrim {
  /**
  * Instancia um comportamento scrim
  * @param {object} - Objeto de configuração inicial para destructuring
  * @property {object} trigger - Elemento DOM que representa o acionador do comportmento scrim
  * @property {string} closeElement - Elemento Dom do trigger que fecha o scrim
  * @property {boolean} escEnable - Habilita a tecla ESC do teclado para fechar o scrim
  * @property {boolean} limitTabKey - Impede a navegação via tab fora da modal
  */
  constructor({ trigger, closeElement='', escEnable=false , limitTabKey=false}) {
    this.trigger = trigger
    this.escEnable = escEnable
    this.limitTabKey = limitTabKey
    this.closeElement = this.elementHideScrim(closeElement)
    if (this.trigger) {
      this.setBehavior()
    }
  }

  /**
  * Alterna o estado de visualização do comportamento scrim
  * @private
  */
  showScrim(){
    if (this.trigger) {
      this.trigger.classList.add('active')
      if(this.trigger.children.length>0){
      const firstChild = this.trigger.children[0]
        firstChild.setAttribute('aria-modal','true')
        firstChild.setAttribute('role','dialog')
        firstChild.setAttribute('data-visible', "true")
      }
      this._setFocusFirstElement()
      if(this.limitTabKey){
        this.limitTabNavigation()
      }
    }
  }

 /**
  * Ativa o foco para o primeiro elemento com zindex maior ou igual a zero
  * @private
  */
_setFocusFirstElement(){
  const  internalElments =this._getInternalElementsFocusable()
  if(internalElments.length>0){
    internalElments[0].focus()
  }
}

  /**
  * Limita a navegação via Tab
  * @private
  */
limitTabNavigation(){
  document.addEventListener('focusin', function (e) {
    let elementfocus = e.target
    var isInternalElemnt = false
    const  internalElments =this._getInternalElementsFocusable()
    internalElments.forEach(function(element){
      if(elementfocus==element){
        isInternalElemnt = true
      }
    }
    );
    if(!isInternalElemnt){
      e.preventDefault();
      this._setFocusFirstElement()
    }
  }.bind(this))
}

  /**
  * retorna os elementos internos que podem receber o estado de foco
  * @private
  */
_getInternalElementsFocusable(){
  return Array.from(this.trigger.querySelectorAll('*')).filter((element) => {
    return element.tabIndex >= 0;
  })
}

  /**
  * Alterna o estado de escondido do comportamento scrim
  * @private
  */
  hideScrim() {
    this.trigger.classList.remove('active')
    this.trigger.setAttribute('data-visible', false)
  }

  /**
  * Seta o elemento Dom que vai fechar o scrim e adiciona o listener para fechar com ESC
  * @public
  */
  elementHideScrim(element) {
    this.hideElements(element);
    this.addEscapeListener();
  }

    /**
  * Seta o elemento Dom que vai fechar o scrim
  * @public
  */
  hideElements(element) {
    if(element){
      this.trigger.querySelectorAll([element]).forEach((element) => {
        this.closeElement = element;
        this._setCloseClick();
      });
    }
    this.trigger.querySelectorAll('[data-dismiss=true]').forEach((item) => {
      this.closeElement = item;
      this._setCloseClick();
    });
  }
    /**
  * Adiciona um listener para fechar o scrim com ESC quando o escEnable estiver como true
  */
  addEscapeListener() {
    if (this.escEnable) {
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
          this.hideScrim();
        }
      });
    }
  }

  /**
  * Adiciona listener de fechamento no elemento que fecha o scrim
  * @private
  */
  _setCloseClick() {
    this.closeElement.addEventListener('click', () => {
      this.hideScrim()
    })
  }
  /**
  * Configura o comportamento scrim
  * @public
  */
  setBehavior() {
    this.trigger.addEventListener('click', (event) => {
      if (event.target.getAttribute('data-scrim')) {
        this.hideScrim()
      }
    })
  }
}
