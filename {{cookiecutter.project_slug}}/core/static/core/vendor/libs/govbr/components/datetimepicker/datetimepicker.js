import flatpickr from 'flatpickr'
const Brazilian = require('flatpickr/dist/l10n/pt').default.pt

/** Classe para instanciar um objeto BRDateTimePicker*/
class BRDateTimePicker {
  /**
   * Instancia do objeto
   * @param {string} name - Nome do componente em minúsculo
   * @param {object} component - Objeto referenciando a raiz do componente DOM
   * @param {string} config - atributo de configuração do componente
   * @param {object} language arquivo de linguagem do flatpick por padrão nesse componente vem portugues
   */
  constructor(name, component, config, language = Brazilian) {
    this.name = name
    this.component = component
    this.language = language

    this.component.addEventListener('blur', () => {
      if (!isNaN(new Date(this.component.value))) {
        fp.setDate(this.component.value)
      }
    })

    this.component.addEventListener('keyup', () => {
      if (!isNaN(new Date(this.component.value))) {
        // if the cursor is at the end of the edit and we have a full sized date, allow the date to immediately change, otherwise just move to the correct month without actually changing it
        if (this.component.selectionStart >= 10)
          fp.setDate(this.component.value)
        else fp.jumpToDate(this.component.value)
      }
    })
    // localization global
    flatpickr.localize(language)

    this.configAttribute = this.component.getAttribute('datetimepicker-config')

    if (this.configAttribute) {
      // Transforma o atributo em um objeto
      const properties = this.configAttribute.split(',')
      this.obj = []
      properties.forEach((element) => {
        const tup = element.split(':')
        this.obj[tup[0]] = tup[1].replaceAll("'", '').trim() // eslint-disable-line

        this.saida = this.obj
      }, this)

      this.config = this.obj
    } else {
      this.config = config
    }

    this._buildDateTimePicker()
  }
  /**
   * Adiciona máscara de data no input
   * @param {*} elm
   */
  _dateInputMask(elm) {
    elm.setAttribute('maxlength', 10)
    elm.addEventListener('keypress', (e) => {
      if (e.keyCode < 47 || e.keyCode > 57) {
        e.preventDefault()
      }

      const len = elm.value.length

      if (len !== 1 || len !== 3) {
        if (e.keyCode == 47) {
          e.preventDefault()
        }
      }

      if (len === 2) {
        elm.value += '/'
      }

      if (len === 5) {
        elm.value += '/'
      }
    })
  }
  /**
   *  Adiciona máscara de hora no input
   * @param {*} elm * Dom do elemento input
   */
  _dateTimeInputMask(elm) {
    elm.setAttribute('maxlength', 16)
    elm.addEventListener('keypress', (e) => {
      if (e.keyCode < 47 || e.keyCode > 57) {
        e.preventDefault()
      }

      const len = elm.value.length

      if (len !== 1 || len !== 3) {
        if (e.keyCode == 47) {
          e.preventDefault()
        }
      }
      switch (len) {
        case 2:
          elm.value += '/'
          break
        case 5:
          elm.value += '/'
          break
        case 10:
          elm.value += ' '
          break
        case 13:
          elm.value += ':'
          break

        default:
          break
      }
    })
  }
  /**
   * Coloca máscara com range de data no input
   * @param {*} elm * Dom do elemento input
   */
  _dateRangeInputMask(elm) {
    elm.setAttribute('maxlength', 25)
    elm.addEventListener('keypress', (e) => {
      if (e.keyCode < 47 || e.keyCode > 57) {
        e.preventDefault()
      }

      const len = elm.value.length

      if (len !== 1 || len !== 3) {
        if (e.keyCode === 47) {
          e.preventDefault()
        }
      }
      this._positionRangeMask(elm, len)
    })
  }
  /**
   * Insere a máscara na Dom
   * @param {*} elm Dom do elemento input
   * @param {*} len Tamanho do elemento inserido
   */
  _positionRangeMask(elm, len) {
    const tamSeparator = this.language.rangeSeparator.length
    const daySeparator = 10 + tamSeparator + 2
    const monthSeparator = 10 + tamSeparator + 5
    elm.setAttribute('maxlength', 20 + tamSeparator)

    switch (len) {
      case 2:
        elm.value += '/'
        break
      case 5:
        elm.value += '/'
        break
      case 10:
        elm.value += this.language.rangeSeparator
        break
      case daySeparator:
        elm.value += '/'
        break
      case monthSeparator:
        elm.value += '/'
        break

      default:
        break
    }
  }
  /**
   * Insere máscara de hora
   *
   * @param {*} elm dom do elemento input
   */
  _timeInputMask(elm) {
    elm.setAttribute('maxlength', 5)
    elm.addEventListener('keypress', (e) => {
      if (e.keyCode < 47 || e.keyCode > 57) {
        e.preventDefault()
      }

      const len = elm.value.length

      if (len !== 1 || len !== 3) {
        if (e.keyCode === 47) {
          e.preventDefault()
        }
      }

      if (len === 2) {
        elm.value += ':'
      }
    })
  }

  /**
   * Formata o componente e monta instância flatpickr
   * @private
   */
  _buildDateTimePicker() {
    let format = 'd/m/Y'
    let time = false
    let noCalendar = false

    switch (this.component.getAttribute('data-type')) {
      case 'date':
        format = 'd/m/Y'
        time = false
        noCalendar = false
        this._dateInputMask(this.component.querySelectorAll('input')[0])
        break

      case 'time':
        format = 'H:i'
        time = true
        noCalendar = true
        this._timeInputMask(this.component.querySelectorAll('input')[0])
        break
      case 'datetime-local':
        format = 'd/m/Y H:i'
        time = true
        noCalendar = false
        this._dateTimeInputMask(this.component.querySelectorAll('input')[0])
        break
      case 'datetime-range':
        format = 'd/m/Y'
        time = false
        noCalendar = false
        this._dateRangeInputMask(this.component.querySelectorAll('input')[0])
        break
      default:
        format = 'd/m/Y'
        time = false
        noCalendar = false
        if (this.component.getAttribute('data-mode') === 'range') {
          this._dateRangeInputMask(this.component.querySelectorAll('input')[0])
        } else {
          this._dateInputMask(this.component.querySelectorAll('input')[0])
        }
        break
    }

    this.config_native = {
      allowInput: true,
      dateFormat: format,
      disableMobile: 'true',
      enableTime: time,
      minuteIncrement: 1,

      mode: this.component.getAttribute('data-mode'),
      nextArrow:
        '<button class="br-button circle small" type="button"><i class="fas fa-chevron-right"></i></button>',
      noCalendar: noCalendar,
      prevArrow:
        '<button class="br-button circle small" type="button"><i class="fas fas fa-chevron-left"></i></button>',
      time_24hr: true,
      wrap: true,
    }
    this.config_flatpick = Object.assign(this.config, this.config_native)

    this.calendar = flatpickr(
      this.component,
      Object.assign(this.config, this.config_native)
    )

    this.calendar.config.onOpen.push(() => {
      document.querySelectorAll('.arrowUp').forEach((element) => {
        element.classList.add('fas', 'fa-chevron-up')
      })
      document.querySelectorAll('.arrowDown').forEach((element) => {
        element.classList.add('fas', 'fa-chevron-down')
      })
    })
  }
}

export default BRDateTimePicker
