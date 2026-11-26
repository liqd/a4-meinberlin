import L from 'leaflet'
import Modal from 'bootstrap/js/dist/modal'
import django from 'django'

const translations = {
  duplicate: django.gettext('This map layer has already been added.'),
  invalid: django.gettext('The link does not lead to a usable map layer.'),
  nameRequired: django.gettext('Please enter a name for the map layer.'),
  layerRequired: django.gettext('Please choose a map layer.'),
  added: django.gettext('Map layer added.'),
  updated: django.gettext('Map layer updated.'),
  removed: django.gettext('Map layer removed.'),
  selected: django.gettext('Map layer selected.'),
  deselected: django.gettext('Map layer deselected.')
}

const Leaflet = window.L || L
const choosePolygonMaps = new Map()
const historyReloadFlag = 'mbAreaSettingsReloaded'
let presetConfirmPatched = false

function normalizeOpacity (value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return 100
  return Math.max(0, Math.min(100, Math.round(number / 10) * 10))
}

function arrivedFromHistory () {
  try {
    if (window.performance && window.performance.getEntriesByType) {
      const entries = window.performance.getEntriesByType('navigation')
      if (entries && entries.length) {
        return entries[0].type === 'back_forward'
      }
    }
    const legacy = window.performance && window.performance.navigation
    return Boolean(legacy && legacy.type === 2)
  } catch (e) {
    return false
  }
}

Leaflet.Map.addInitHook(function () {
  const container = this.getContainer()
  if (container && container.dataset.map === 'choose_polygon') {
    const name = container.dataset.name || 'polygon'
    choosePolygonMaps.set(name, this)
    document.dispatchEvent(
      new CustomEvent('a4:map-ready', {
        detail: { map: this, container, name }
      })
    )
  }
})

function getChoosePolygonMap () {
  if (choosePolygonMaps.has('polygon')) {
    return choosePolygonMaps.get('polygon')
  }
  return choosePolygonMaps.values().next().value
}

function init () {
  const wrapper = document.querySelector('[data-map-layers]')
  if (!wrapper) return

  // Returning via back/forward lets the browser repopulate form controls with
  // values that were never saved. Reload once so the page reflects the server.
  try {
    if (arrivedFromHistory()) {
      if (!window.sessionStorage.getItem(historyReloadFlag)) {
        window.sessionStorage.setItem(historyReloadFlag, '1')
        window.location.replace(window.location.href)
        return
      }
    }
    window.sessionStorage.removeItem(historyReloadFlag)
  } catch (e) {
    // Ignore storage errors and fall through to the normal reset logic.
  }

  const list = wrapper.querySelector('[data-map-layers-list]')
  const hiddenLayers = wrapper.querySelector('input[name="map_layers"]')
  const hiddenSelected = wrapper.querySelector(
    'input[name="selected_map_layer"]'
  )
  const status = wrapper.querySelector('[data-map-layers-status]')
  const resolveEndpoint = wrapper.dataset.resolveUrl
  if (!list || !hiddenLayers || !hiddenSelected || !resolveEndpoint) return

  const addModalEl = document.getElementById('map-layer-add-modal')
  const editModalEl = document.getElementById('map-layer-edit-modal')
  const deleteModalEl = document.getElementById('map-layer-delete-modal')
  if (!addModalEl || !editModalEl || !deleteModalEl) return

  const addModal = new Modal(addModalEl)
  const editModal = new Modal(editModalEl)
  const deleteModal = new Modal(deleteModalEl)
  const modalState = new WeakMap()
  const wmsUrlPattern = /^https:\/\/gdi\.berlin\.de\/services\/wms\/[A-Za-z0-9._-]+/

  const state = {
    layers: readLayers(hiddenLayers.value),
    selected: hiddenSelected.value || '',
    removeIndex: null,
    activeWmsLayer: null,
    activeWmsKey: '',
    activeWmsOpacity: null
  }

  function readLayers (value) {
    try {
      const layers = JSON.parse(value || '[]')
      if (!Array.isArray(layers)) return []
      return layers
        .filter((layer) => layer && typeof layer === 'object')
        .map((layer) => {
          const serviceUrl = String(layer.service_url || '')
          const layerName = String(layer.layer_name || '')
          return {
            name: String(layer.name || layer.title || layerName),
            service_url: serviceUrl,
            layer_name: layerName,
            title: String(layer.title || ''),
            attribution: String(layer.attribution || ''),
            is_available: layer.is_available !== false,
            opacity: normalizeOpacity(layer.opacity),
            key: String(layer.key || `${serviceUrl}|${layerName}`)
          }
        })
    } catch (e) {
      return []
    }
  }

  function writeState (notify) {
    hiddenLayers.value = JSON.stringify(state.layers)
    hiddenSelected.value = state.selected
    renderList()
    updateMapPreview()
    if (notify) {
      // Let the dashboard "unsaved changes" watcher know about staged edits.
      hiddenSelected.dispatchEvent(new window.Event('change', { bubbles: true }))
    }
  }

  function announce (message) {
    if (!status) return
    status.textContent = ''
    window.setTimeout(() => {
      status.textContent = message
    }, 0)
  }

  function shortUrl (url) {
    return url.replace(/^https:\/\//, '')
  }

  function renderList () {
    list.innerHTML = ''

    const noneItem = document.createElement('li')
    noneItem.className = 'map-layers__item map-layers__item--none'
    const noneLabel = document.createElement('label')
    noneLabel.className = 'map-layers__label'
    noneLabel.htmlFor = 'map-layer-none'
    const noneRadio = document.createElement('input')
    noneRadio.className = 'form-check-input'
    noneRadio.type = 'radio'
    noneRadio.name = 'map-layer-selection'
    noneRadio.id = 'map-layer-none'
    noneRadio.value = ''
    noneRadio.checked = !state.selected
    noneRadio.dataset.mapLayerNone = ''
    const noneText = document.createElement('span')
    noneText.className = 'map-layers__name'
    noneText.textContent = django.gettext('No map layer')
    noneLabel.appendChild(noneRadio)
    noneLabel.appendChild(noneText)
    noneItem.appendChild(noneLabel)
    list.appendChild(noneItem)

    if (!state.layers.length) {
      const empty = document.createElement('li')
      empty.className = 'map-layers__empty'
      empty.dataset.mapLayersEmpty = ''
      empty.textContent = django.gettext('No map layer has been added yet.')
      list.appendChild(empty)
      return
    }

    state.layers.forEach((layer, index) => {
      const item = document.createElement('li')
      item.className = 'map-layers__item'
      item.dataset.mapLayer = ''
      item.dataset.index = String(index)

      const details = document.createElement('div')
      details.className = 'map-layers__details'

      const label = document.createElement('label')
      label.className = 'map-layers__label'
      label.htmlFor = `map-layer-radio-${index}`

      const radio = document.createElement('input')
      radio.className = 'form-check-input'
      radio.type = 'radio'
      radio.name = 'map-layer-selection'
      radio.id = `map-layer-radio-${index}`
      radio.value = layer.key
      radio.checked = layer.key === state.selected

      const name = document.createElement('span')
      name.className = 'map-layers__name'
      name.textContent = layer.name

      const text = document.createElement('span')
      text.className = 'map-layers__text'
      text.appendChild(name)

      const url = document.createElement('span')
      url.className = 'map-layers__url'
      url.title = layer.service_url
      url.textContent = shortUrl(layer.service_url)
      text.appendChild(url)

      if (!layer.is_available) {
        const warning = document.createElement('span')
        warning.className = 'map-layers__warning'
        const icon = document.createElement('i')
        icon.className = 'fas fa-exclamation-triangle'
        icon.setAttribute('aria-hidden', 'true')
        warning.appendChild(icon)
        warning.appendChild(
          document.createTextNode(
            django.gettext('This map layer could not be loaded.')
          )
        )
        text.appendChild(warning)
      }

      label.appendChild(radio)
      label.appendChild(text)
      details.appendChild(label)

      const actions = document.createElement('div')
      actions.className = 'map-layers__actions'

      const edit = document.createElement('button')
      edit.type = 'button'
      edit.className = 'map-layers__action'
      edit.dataset.mapLayerEdit = ''
      edit.innerHTML = '<i class="fas fa-pencil-alt" aria-hidden="true"></i> '
      edit.appendChild(document.createTextNode(django.gettext('Edit')))

      const remove = document.createElement('button')
      remove.type = 'button'
      remove.className = 'map-layers__action'
      remove.dataset.mapLayerRemove = ''
      remove.innerHTML = '<i class="fas fa-trash-alt" aria-hidden="true"></i> '
      remove.appendChild(document.createTextNode(django.gettext('Remove')))

      actions.appendChild(edit)
      actions.appendChild(remove)
      item.appendChild(details)
      item.appendChild(actions)
      list.appendChild(item)
    })
  }

  function setPresetSelect (value) {
    const presetSelect = document.getElementById('select_polygon')
    if (!presetSelect) return

    const $ = window.jQuery
    if ($ && $.fn.select2) {
      // Update select2's display without firing the form's change watcher.
      $(presetSelect).val(value).trigger('change.select2')
    } else {
      presetSelect.value = value
    }
  }

  function syncPolygonField () {
    const form = wrapper.closest('form')
    if (!form) return

    const polygonInput = form.querySelector('input[name="polygon"]')
    if (polygonInput && polygonInput.value !== polygonInput.defaultValue) {
      polygonInput.value = polygonInput.defaultValue
    }

    // The preset dropdown is only a helper for drawing; it always starts blank
    // and the map shows the stored polygon.
    setPresetSelect('')
  }

  function hasRestoredState () {
    if (hiddenLayers.value !== (hiddenLayers.defaultValue || '[]')) return true
    if (hiddenSelected.value !== (hiddenSelected.defaultValue || '')) return true

    // A restored radio can differ even when the hidden fields do not.
    const checked = list.querySelector(
      'input[name="map-layer-selection"]:checked'
    )
    if ((checked ? checked.value : '') !== state.selected) return true

    const form = wrapper.closest('form')
    const polygonInput = form && form.querySelector('input[name="polygon"]')
    return Boolean(polygonInput && polygonInput.value !== polygonInput.defaultValue)
  }

  function syncFromServer () {
    const serverLayers = hiddenLayers.defaultValue || '[]'
    const serverSelected = hiddenSelected.defaultValue || ''
    hiddenLayers.value = serverLayers
    hiddenSelected.value = serverSelected
    state.layers = readLayers(serverLayers)
    state.selected = serverSelected
    state.removeIndex = null

    syncPolygonField()

    if (state.activeWmsLayer) {
      const map = getChoosePolygonMap()
      if (map) map.removeLayer(state.activeWmsLayer)
      state.activeWmsLayer = null
      state.activeWmsKey = ''
      state.activeWmsOpacity = null
    }
    writeState()
  }

  function allowPresetReplacement () {
    if (presetConfirmPatched) return
    presetConfirmPatched = true

    const nativeConfirm = window.confirm
    if (!nativeConfirm) return

    const message = django.gettext(
      'Do you want to load this preset and delete all the existing polygons?'
    )
    window.confirm = function (prompt) {
      // Replacing a preset is an explicit choice; skip the core dialog.
      if (prompt === message) return true
      return nativeConfirm.call(window, prompt)
    }
  }

  function getSelectedLayer () {
    return state.layers.find((layer) => layer.key === state.selected)
  }

  function updateMapPreview () {
    const map = getChoosePolygonMap()
    if (!map) return

    const layer = getSelectedLayer()
    if (!layer) {
      if (state.activeWmsLayer) {
        map.removeLayer(state.activeWmsLayer)
        state.activeWmsLayer = null
        state.activeWmsKey = ''
        state.activeWmsOpacity = null
      }
      return
    }
    const opacity = normalizeOpacity(layer.opacity) / 100
    if (state.activeWmsKey === layer.key && state.activeWmsOpacity === opacity) {
      return
    }

    if (state.activeWmsLayer) {
      map.removeLayer(state.activeWmsLayer)
    }
    state.activeWmsLayer = Leaflet.tileLayer.wms(layer.service_url, {
      layers: layer.layer_name,
      format: 'image/png',
      transparent: true,
      version: '1.3.0',
      attribution: layer.attribution,
      opacity
    })
    state.activeWmsLayer.setZIndex(1)
    state.activeWmsLayer.addTo(map)
    state.activeWmsKey = layer.key
    state.activeWmsOpacity = opacity
  }

  function layerKey (serviceUrl, layerName) {
    return `${serviceUrl}|${layerName}`
  }

  function getModalState (modalEl) {
    let value = modalState.get(modalEl)
    if (!value) {
      value = {
        resolved: null,
        layerName: '',
        autoName: '',
        editingIndex: null,
        resolvedUrl: '',
        fallback: null,
        opacity: 100,
        abort: null
      }
      modalState.set(modalEl, value)
    }
    return value
  }

  function modalParts (modalEl) {
    return {
      url: modalEl.querySelector('[data-map-layer-url]'),
      name: modalEl.querySelector('[data-map-layer-name]'),
      select: modalEl.querySelector('[data-map-layer-select]'),
      selectGroup: modalEl.querySelector('[data-map-layer-select-group]'),
      error: modalEl.querySelector('[data-map-layer-error]'),
      spinner: modalEl.querySelector('[data-map-layer-spinner]'),
      opacityGroup: modalEl.querySelector('[data-map-layer-opacity-group]'),
      opacityValue: modalEl.querySelector('[data-map-layer-opacity-value]'),
      opacityIncrease: modalEl.querySelector(
        '[data-map-layer-opacity-increase]'
      ),
      opacityDecrease: modalEl.querySelector(
        '[data-map-layer-opacity-decrease]'
      ),
      save: modalEl.querySelector('[data-map-layer-save]')
    }
  }

  function clearError (modalEl) {
    const parts = modalParts(modalEl)
    parts.error.textContent = ''
    parts.url.removeAttribute('aria-invalid')
  }

  function showError (modalEl, message) {
    const parts = modalParts(modalEl)
    parts.error.textContent = message
    parts.url.setAttribute('aria-invalid', 'true')
  }

  function setBusy (modalEl, busy) {
    const parts = modalParts(modalEl)
    parts.spinner.hidden = !busy
    parts.url.setAttribute('aria-busy', busy ? 'true' : 'false')
  }

  function setModalOpacity (modalEl, opacity) {
    const parts = modalParts(modalEl)
    const controller = getModalState(modalEl)
    controller.opacity = normalizeOpacity(opacity)
    const transparency = 100 - controller.opacity
    if (parts.opacityValue) {
      parts.opacityValue.textContent = `${transparency} %`
    }
  }

  function resetModal (modalEl) {
    const parts = modalParts(modalEl)
    const controller = getModalState(modalEl)
    if (controller.abort) controller.abort.abort()
    controller.resolved = null
    controller.layerName = ''
    controller.autoName = ''
    controller.editingIndex = null
    controller.resolvedUrl = ''
    controller.fallback = null
    controller.abort = null
    parts.url.value = ''
    parts.name.value = ''
    parts.select.value = ''
    parts.select.innerHTML = `<option value="">${django.gettext('Please choose a layer')}</option>`
    parts.selectGroup.hidden = true
    parts.opacityGroup.hidden = true
    setModalOpacity(modalEl, 100)
    parts.save.disabled = true
    clearError(modalEl)
    setBusy(modalEl, false)
  }

  function setAutoName (modalEl, title) {
    const parts = modalParts(modalEl)
    const controller = getModalState(modalEl)
    const previous = controller.autoName
    const current = parts.name.value.trim()
    controller.autoName = title || ''
    if (!current || current === previous) {
      parts.name.value = title || ''
    }
  }

  function selectLayer (modalEl, layerName) {
    const controller = getModalState(modalEl)
    controller.layerName = layerName
    const layer = controller.resolved
      ? controller.resolved.layers.find((item) => item.name === layerName)
      : null
    if (layer) setAutoName(modalEl, layer.title)
    updateSaveState(modalEl)
  }

  function updateSaveState (modalEl) {
    const parts = modalParts(modalEl)
    const controller = getModalState(modalEl)
    parts.save.disabled = !(
      controller.resolved &&
      controller.layerName &&
      parts.name.value.trim()
    )
  }

  function populateLayerSelect (modalEl, layers) {
    const parts = modalParts(modalEl)
    parts.select.innerHTML = `<option value="">${django.gettext('Please choose a layer')}</option>`
    layers.forEach((layer) => {
      const option = document.createElement('option')
      option.value = layer.name
      option.textContent = layer.title
      parts.select.appendChild(option)
    })
  }

  async function resolveUrl (modalEl) {
    const parts = modalParts(modalEl)
    const controller = getModalState(modalEl)
    const url = parts.url.value.trim()
    const preferred = controller.layerName

    clearError(modalEl)
    controller.resolved = null
    controller.layerName = ''
    parts.save.disabled = true
    parts.opacityGroup.hidden = true
    if (!url) {
      parts.selectGroup.hidden = true
      return
    }

    if (controller.abort) controller.abort.abort()
    controller.abort = new window.AbortController()
    const abort = controller.abort
    setBusy(modalEl, true)

    try {
      const response = await window.fetch(resolveEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ url }),
        signal: abort.signal
      })
      const data = await response.json().catch(() => ({}))
      if (!response.ok || !data.ok) {
        throw new Error(data.message || translations.invalid)
      }
      if (url !== parts.url.value.trim()) return

      controller.resolved = data
      controller.resolvedUrl = url
      parts.opacityGroup.hidden = false
      if (data.layers.length === 1) {
        parts.selectGroup.hidden = true
        selectLayer(modalEl, data.layers[0].name)
      } else {
        parts.selectGroup.hidden = false
        populateLayerSelect(modalEl, data.layers)
        if (
          preferred &&
          data.layers.some((layer) => layer.name === preferred)
        ) {
          parts.select.value = preferred
          selectLayer(modalEl, preferred)
        } else {
          setAutoName(modalEl, data.service_title)
          updateSaveState(modalEl)
        }
      }
    } catch (error) {
      if (error.name === 'AbortError') return
      controller.resolved = controller.fallback
      controller.layerName = controller.fallback
        ? preferred || controller.fallback.layers[0].name
        : ''
      updateSaveState(modalEl)
      if (controller.fallback) parts.opacityGroup.hidden = false
      showError(modalEl, error.message || translations.invalid)
    } finally {
      if (controller.abort === abort) {
        controller.abort = null
        setBusy(modalEl, false)
        updateSaveState(modalEl)
      }
    }
  }

  function getCsrfToken () {
    const input = document.querySelector('[name=csrfmiddlewaretoken]')
    return input ? input.value : ''
  }

  function startAdd () {
    resetModal(addModalEl)
    addModal.show()
    const parts = modalParts(addModalEl)
    window.setTimeout(() => parts.url.focus(), 150)
  }

  function startEdit (index) {
    const layer = state.layers[index]
    if (!layer) return

    resetModal(editModalEl)
    const parts = modalParts(editModalEl)
    const controller = getModalState(editModalEl)
    controller.editingIndex = index
    controller.fallback = {
      service_url: layer.service_url,
      service_title: layer.title,
      layers: [
        {
          name: layer.layer_name,
          title: layer.title || layer.name,
          attribution: layer.attribution
        }
      ]
    }
    controller.resolved = controller.fallback
    controller.layerName = layer.layer_name
    controller.autoName = layer.title || layer.name
    setModalOpacity(editModalEl, layer.opacity)
    parts.url.value = layer.service_url
    parts.name.value = layer.name
    parts.save.disabled = false
    editModal.show()
    resolveUrl(editModalEl)
  }

  function startRemove (index) {
    const layer = state.layers[index]
    if (!layer) return
    state.removeIndex = index
    const name = deleteModalEl.querySelector('[data-map-layer-delete-name]')
    if (name) name.textContent = layer.name
    deleteModal.show()
  }

  function saveModal (modalEl) {
    const parts = modalParts(modalEl)
    const controller = getModalState(modalEl)
    if (controller.abort) {
      showError(
        modalEl,
        django.gettext('Please wait until the link has been checked.')
      )
      return
    }
    if (!controller.resolved) {
      resolveUrl(modalEl)
      return
    }
    if (!controller.layerName) {
      showError(modalEl, translations.layerRequired)
      return
    }

    const name = parts.name.value.trim()
    if (!name) {
      showError(modalEl, translations.nameRequired)
      return
    }

    const serviceUrl = controller.resolved.service_url
    const key = layerKey(serviceUrl, controller.layerName)
    const duplicate = state.layers.some(
      (layer, index) => index !== controller.editingIndex && layer.key === key
    )
    if (duplicate) {
      showError(modalEl, translations.duplicate)
      return
    }

    const serviceLayer = controller.resolved.layers.find(
      (layer) => layer.name === controller.layerName
    )
    const layer = {
      name,
      service_url: serviceUrl,
      layer_name: controller.layerName,
      title: serviceLayer ? serviceLayer.title : '',
      attribution: serviceLayer ? serviceLayer.attribution || '' : '',
      is_available: true,
      opacity: controller.opacity,
      key
    }

    if (controller.editingIndex === null) {
      state.layers.push(layer)
      if (!state.selected) state.selected = key
      announce(translations.added)
      addModal.hide()
    } else {
      const index = controller.editingIndex
      const oldKey = state.layers[index].key
      state.layers[index] = layer
      if (state.selected === oldKey) state.selected = key
      announce(translations.updated)
      editModal.hide()
    }
    writeState(true)
  }

  function confirmRemove () {
    if (state.removeIndex === null) return
    const layer = state.layers[state.removeIndex]
    if (!layer) return
    state.layers.splice(state.removeIndex, 1)
    if (state.selected === layer.key) {
      state.selected = ''
      announce(translations.deselected)
    } else {
      announce(translations.removed)
    }
    state.removeIndex = null
    deleteModal.hide()
    writeState(true)
  }

  list.addEventListener('change', (event) => {
    if (!event.target.matches('input[name="map-layer-selection"]')) return
    state.selected = event.target.checked ? event.target.value : ''
    hiddenSelected.value = state.selected
    updateMapPreview()
    announce(state.selected ? translations.selected : translations.deselected)
  })

  list.addEventListener('click', (event) => {
    const item = event.target.closest('[data-map-layer]')
    if (!item) return
    const index = Number(item.dataset.index)
    if (event.target.closest('[data-map-layer-edit]')) {
      startEdit(index)
    } else if (event.target.closest('[data-map-layer-remove]')) {
      startRemove(index)
    }
  })

  const addButton = wrapper.querySelector('[data-map-layer-add]')
  if (addButton) addButton.addEventListener('click', startAdd)

  addModalEl.addEventListener('shown.bs.modal', () => {
    modalParts(addModalEl).url.focus()
  })
  editModalEl.addEventListener('shown.bs.modal', () => {
    modalParts(editModalEl).name.focus()
  })

  addModalEl.addEventListener('hidden.bs.modal', () => resetModal(addModalEl))
  editModalEl.addEventListener('hidden.bs.modal', () => {
    resetModal(editModalEl)
  })

  const modalElements = [addModalEl, editModalEl]
  modalElements.forEach((modalEl) => {
    const parts = modalParts(modalEl)
    const controller = getModalState(modalEl)

    let resolveTimer = null
    parts.url.addEventListener('paste', () => {
      window.clearTimeout(resolveTimer)
      window.setTimeout(() => resolveUrl(modalEl), 0)
    })
    parts.url.addEventListener('blur', () => {
      window.clearTimeout(resolveTimer)
      if (!controller.resolved) {
        resolveUrl(modalEl)
      }
    })
    parts.url.addEventListener('input', () => {
      window.clearTimeout(resolveTimer)
      clearError(modalEl)
      const value = parts.url.value.trim()
      if (value === controller.resolvedUrl) return
      controller.resolved = null
      controller.resolvedUrl = ''
      controller.fallback = null
      controller.layerName = ''
      parts.save.disabled = true
      parts.selectGroup.hidden = true
      parts.opacityGroup.hidden = true
      setModalOpacity(modalEl, 100)
      if (!wmsUrlPattern.test(value)) return
      // Re-check while typing once the value looks like a full service link.
      resolveTimer = window.setTimeout(() => {
        if (parts.url.value.trim() === value) {
          resolveUrl(modalEl)
        }
      }, 500)
    })
    parts.select.addEventListener('change', () => {
      selectLayer(modalEl, parts.select.value)
    })
    parts.opacityIncrease.addEventListener('click', () => {
      setModalOpacity(modalEl, controller.opacity - 10)
    })
    parts.opacityDecrease.addEventListener('click', () => {
      setModalOpacity(modalEl, controller.opacity + 10)
    })
    parts.name.addEventListener('input', () => {
      clearError(modalEl)
      updateSaveState(modalEl)
    })
    parts.save.addEventListener('click', () => saveModal(modalEl))
  })

  const deleteConfirm = deleteModalEl.querySelector(
    '[data-map-layer-delete-confirm]'
  )
  if (deleteConfirm) deleteConfirm.addEventListener('click', confirmRemove)

  allowPresetReplacement()
  syncFromServer()

  // Browsers may restore form controls (including radios) after our init, or
  // restore the whole page from bfcache. Discard anything that was not saved.
  const restoreFromServer = () => {
    if (hasRestoredState()) {
      syncFromServer()
    } else {
      // A restored <select> is not detectable reliably, so always re-assert
      // the blank preset selection.
      syncPolygonField()
    }
  }

  window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
      // Restored from bfcache: reload so unsaved values are discarded.
      window.location.replace(window.location.href)
      return
    }
    restoreFromServer()
    window.setTimeout(restoreFromServer, 0)
  })

  // Some browsers restore form controls as late as the load event.
  window.addEventListener('load', () => {
    window.setTimeout(restoreFromServer, 0)
  })

  document.addEventListener('a4:map-ready', updateMapPreview)
}

document.addEventListener(
  'DOMContentLoaded',
  function () {
    window.setTimeout(init, 0)
  },
  false
)
document.addEventListener(
  'a4.embed.ready',
  function () {
    window.setTimeout(init, 0)
  },
  false
)
