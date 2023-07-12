import BRTooltip from '../../components/tooltip/tooltip'
/** Classe para instanciar um objeto BRUpload */
class BRUpload {
  /**
   * @param {*} name nome do componente
   * @param {*} component componente
   * @param {*} uploadFiles  promisse de status do upload
   */
  constructor(name, component, uploadFiles) {
    this.name = name
    this.component = component
    this._inputElement = this.component.querySelector('.upload-input')
    this._fileList = this.component.querySelector('.upload-list')
    this._btnUpload = this.component.querySelector('.upload-button')
    this._label = this.component.querySelector('label')
    this._textHelp = document.querySelector('.text-base')
    this._fileArray = []
    this._uploadFiles = uploadFiles
    this._setBehavior()
  }

  /**
   * Define comportamentos do componente
   * @private
   */
  _setBehavior() {
    if (this._inputElement) {
      const button = document.createElement('button')
      button.className = 'upload-button'
      button.setAttribute('type', 'button')

      if (this._inputElement.getAttribute('multiple'))
        button.innerHTML =
          '<i class="fas fa-upload" aria-hidden="true"></i><span>Selecione o(s) arquivo(s)</span>'
      else
        button.innerHTML =
          '<i class="fas fa-upload" aria-hidden="true"></i><span>Selecione o arquivo</span>'

      this.component.append(this._label)
      this.component.append(this._inputElement)
      this.component.appendChild(button)
      this.component.append(this._fileList)
      this._btnUpload = this.component.querySelector('.upload-button')
      this._btnUpload.addEventListener(
        'click',
        () => {
          this._clickUpload()
        },
        false
      )
      if (this.component.getAttribute('disabled')) {
        const message = document.createElement('span')
        message.classList.add('feedback', 'warning', 'mt-1')
        message.setAttribute('role', 'alert')
        message.innerHTML =
          '<i class="fas fa-exclamation-triangle" aria-hidden="true"></i>Upload desabilitado'
        this.component.after(message)
      }

      this._fileArray = Array.from(this._inputElement.files)
      this._inputElement.addEventListener(
        'change',
        (event) => {
          this._handleFiles(event)
        },
        false
      )
    }

    this._setDragAndDropBehavior()
  }

  /**
   * Define comportamento de arrastar(drag) e posicionar(drop)
   * @private
   */
  _setDragAndDropBehavior() {
    const uploadButton = this.component.querySelector('.upload-button')

    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
      uploadButton.addEventListener(eventName, this._preventDefaults)
    })
    ;['dragenter', 'dragover'].forEach((eventName) => {
      uploadButton.addEventListener(eventName, this._hightLight.bind(this))
    })
    ;['dragleave', 'drop'].forEach((eventName) => {
      uploadButton.addEventListener(eventName, this._unHightLight.bind(this))
    })

    uploadButton.addEventListener('drop', this._handleDrop.bind(this))
  }

  /**
   * Evita os eventos padrao e propagação de evento
   * @private
   * @param {event} event - referencia ao evento
   */
  _preventDefaults(event) {
    event.preventDefault()
    event.stopPropagation()
  }

  _hightLight() {
    this.component.classList.add('dragging')
  }

  _unHightLight() {
    this.component.classList.remove('dragging')
  }

  /**
   * Ação de posicionar (drop)
   * @private
   * @param {event} event - referencia ao evento
   */
  _handleDrop(event) {
    this.component.classList.remove('dragging')
    const dt = event.dataTransfer
    const { files } = dt
    this._handleFiles(files)
  }

  /**
   * Testa se o objeto que disparou a ação está desabilitado
   * @private
   * @param {event} event - referencia ao evento
   */
  _isDisabled(event) {
    const isDisabled = event.target.getAttribute('disabled')
    if (isDisabled) {
      return true
    } else {
      return false
    }
  }

  /**
   * Simula ação de clicar no input
   * @private
   */
  _clickUpload() {
    this._inputElement.click()
  }

  /**
   * Limpa mensagem de feedback
   * @private
   */
  _removeMessage() {
    for (const message of this.component.querySelectorAll('.feedback')) {
      message.parentNode.removeChild(message)
      message.innerHTML = ''
    }
  }

  /**
   * Remove mensagem de estado
   * @private
   */
  _removeStatus() {
    const remStatus = ['danger', 'warning', 'info', 'success']
    remStatus.forEach((el) => {
      if (this.component.dataset.hasOwnProperty(el))
        this.component.removeAttribute(`data-${el}`)
    })
  }

  /**
   * Define mensagem de feedback
   * @private
   * @param {string} status - estados: danger / info / success / warning
   */
  _feedback(status, text) {
    const icone = `<i class="fas fa-times-circle" aria-hidden="true"></i>${text}`
    const dataStatus = `data-${status}`
    const message = document.createElement('span')
    message.classList.add('feedback', status, 'mt-1')
    message.setAttribute('role', 'alert')
    switch (status) {
      case 'danger':
        message.innerHTML = icone
        break
      case 'info':
        message.innerHTML = icone.replace('fa-times-circle', 'fa-info-circle')
        break
      case 'success':
        message.innerHTML = icone.replace('fa-times-circle', 'fa-check-circle')
        break
      case 'warning':
        message.innerHTML = icone.replace(
          'fa-times-circle',
          'fa-exclamation-triangle'
        )
        break
      default:
        message.innerHTML = ''
    }
    this._removeStatus()
    this.component.setAttribute(dataStatus, dataStatus)
    this._fileList.before(message)
  }

  /**
   * Adiciona arquivos a lista
   * @private
   * @param {File[]} files - lista de arquivos
   */
  _concatFiles(files) {
    const newFiles = !files.length
      ? Array.from(this._inputElement.files)
      : Array.from(files)
    this._fileArray = this._fileArray.concat(newFiles)
  }

  /**
   * Adiciona arquivos a lista
   * @private
   * @param {File[]} files - lista de arquivos
   */
  _handleFiles(files) {
    this._removeMessage()
    if (!this._inputElement.multiple && files.length > 1) {
      this._feedback('danger', 'É permitido o envio de somente 1 arquivo.')
    } else if (!this._inputElement.multiple && this._fileArray.length > 0) {
      this._fileArray = []
      this._concatFiles(files)
      this._updateFileList()
      this._feedback(
        'warning',
        'O arquivo enviado anteriormente foi substituído'
      )
    } else {
      this._concatFiles(files)
      this._updateFileList()
    }
  }

  /**
   * Atualiza lista de arquivos eliminando redundâncias
   * @private
   */
  _updateFileList() {
    this._removeStatus()
    if (this.component.nextElementSibling === this._textHelp) {
      this._textHelp.style.display = 'none'
    }
    if (!this._fileArray.length) {
      this._fileList.innerHTML = ''
      if (this.component.nextElementSibling === this._textHelp) {
        this._textHelp.style.display = ''
      }
    } else {
      this._fileList.innerHTML = ''

      for (let i = 0; i < this._fileArray.length; i++) {
        if ('nowait' in this._fileArray[i]) {
          if (this._fileArray[i].nowait) {
            this._renderItem(i)
          }
        } else if (!this._fileArray[i].requested) {
          this.uploadLoading()
          this.uploadingFile(i)
        }
      }
    }
  }

  /**
   * Mostra mensagem de carregamento
   * @private
   */
  uploadLoading() {
    const loading = document.createElement('div')
    const carga = document.createElement('span')
    carga.classList.add('cargas')
    carga.innerText = 'Carregando...'
    loading.setAttribute('sm', '')
    loading.classList.add('my-3')
    loading.setAttribute('loading', '')
    loading.appendChild(carga)
    this._fileList.appendChild(loading)
  }

  /**
   * Faz upload de arquivo na posição definida
   * @private
   * @param {Number} position - numero do ínidice da posição
   */
  uploadingFile(position) {
    if (this._uploadFiles) {
      this._fileArray[position].requested = true
      this._uploadFiles().then(() => {
        this._fileArray[position].nowait = true
        this._updateFileList()
      })
    }
  }

  /**
   * Renderiza item na posição definida
   * @private
   * @param {Number} position - numero do ínidice da posição
   */
  _renderItem(position) {
    const li = document.createElement('div')
    li.className = 'br-item d-flex'
    this._fileList.appendChild(li)
    li.innerHTML = ''
    const name = document.createElement('div')
    name.className = 'name'
    li.appendChild(name)
    this._fileList.appendChild(li)
    const info = document.createElement('div')
    info.className = 'content'
    info.innerHTML = this._fileArray[position].name
    const tooltip = document.createElement('div')
    tooltip.classList.add('br-tooltip')
    tooltip.setAttribute('role', 'tooltip')
    tooltip.setAttribute('place', 'top')
    tooltip.setAttribute('info', 'info')
    const textTooltip = document.createElement('span')
    textTooltip.classList.add('text')
    textTooltip.setAttribute('role', 'tooltip')
    textTooltip.innerHTML = this._fileArray[position].name
    tooltip.appendChild(textTooltip)
    li.appendChild(info)
    li.appendChild(name)
    li.appendChild(tooltip)
    info.classList.add('text-primary-default', 'mr-auto')
    const del = document.createElement('div')
    del.className = 'support mr-n2'
    const btndel = document.createElement('button')
    const spanSize = document.createElement('span')
    spanSize.className = 'mr-1'
    spanSize.innerHTML = this._calcSize(this._fileArray[position].size)
    del.appendChild(spanSize)
    btndel.className = 'br-button'
    btndel.type = 'button'
    btndel.setAttribute('circle', '')
    btndel.addEventListener(
      'click',
      (event) => {
        this._removeFile(position, event)
      },
      false
    )
    const img = document.createElement('i')
    img.className = 'fa fa-trash'
    btndel.appendChild(img)
    del.appendChild(btndel)
    li.appendChild(del)
    this._fileArray[position].nowait = true
    const tooltipList = []
    for (const brTooltip of window.document.querySelectorAll('.br-tooltip')) {
      tooltipList.push(new BRTooltip('br-tooltip', brTooltip))
    }
  }

  /**
   * Formata tamanho do arquivo
   * @private
   * @param {Number} nBytes - quantidade de bytes do arquivo
   */
  _calcSize(nBytes) {
    let sOutput = ''
    for (
      let aMultiples = ['KB', 'MB', 'GB', 'TB'],
        nMultiple = 0,
        nApprox = nBytes / 1024;
      nApprox > 1;
      nApprox /= 1024, nMultiple++
    ) {
      sOutput = `${nApprox.toFixed(2)} ${aMultiples[nMultiple]}`
    }
    return sOutput
  }

  /**
   * Remove arquivo na posição definida
   * @private
   * @param {Number} index - numero do ínidice da posição
   * @param {event} event - evento que disparou a ação
   */
  _removeFile(index, event) {
    event.stopPropagation()
    event.preventDefault()
    this._removeStatus()
    this._removeMessage()
    this._fileArray.splice(index, 1)
    this._updateFileList()

    if (this._inputElement.multiple)
      this._inputElement.files = this._updateFileListItems(this._fileArray)
    if (!this._inputElement.multiple) this._inputElement.value = ''
  }

  /**
   * Atualiza arquivos da lista
   * @private
   * @param {File[]} files - lista de arquivos
   */
  _updateFileListItems(files) {
    const fileInput = new ClipboardEvent('').clipboardData || new DataTransfer()
    for (let i = 0, len = files.length; i < len; i++)
      fileInput.items.add(files[i])
    return fileInput.files
  }
}

export default BRUpload
