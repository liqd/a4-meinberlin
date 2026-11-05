import django from 'django'
import L from 'leaflet'

import {
  getLayerMode,
  isVectorLayer,
  loadVectorFeatureCollection,
  vectorStyle
} from './map_layers_vector'

const REFRESH_DELAY = 300

const rememberMapInstance = (map) => {
  const container = map.getContainer()
  if (container && container.dataset.map === 'choose_polygon') {
    container.mapLayerMap = map
  }
}

// Leaflet does not expose its map instances on the container. Keep a
// reference so the layer toggles can update the existing area settings map.
L.Map.addInitHook(function () {
  rememberMapInstance(this)
})

const createWmsOverlay = (map, layer) => {
  const overlay = L.tileLayer.wms(layer.url, {
    layers: layer.layer,
    format: 'image/png',
    transparent: true,
    opacity: layer.opacity,
    attribution: layer.attribution,
    className: 'map-layer-overlay'
  })
  overlay.addTo(map)
  return overlay
}

const createVectorOverlay = (map, layer) => {
  const overlay = L.geoJSON(null, {
    style: (feature) => vectorStyle(layer, feature),
    className: 'map-layer-overlay'
  })
  overlay.addTo(map)
  return overlay
}

const init = () => {
  document.querySelectorAll('[data-map="choose_polygon"]').forEach((element) => {
    const map = element.mapLayerMap
    if (!map) {
      return
    }

    let layers = []
    try {
      layers = JSON.parse(element.dataset.mapLayers || '[]')
    } catch {
      layers = []
    }

    const mode = getLayerMode()
    const layersById = new Map(
      layers.map((layer) => [String(layer.id), layer])
    )
    const overlays = new Map()
    const vectorLayers = new Map()
    const form = element.closest('form')
    const checkboxes = form
      ? form.querySelectorAll('input[name="layers"]')
      : []
    const status = form
      ? form.querySelector('[data-map-layer-status]')
      : null

    const refreshVectorLayer = (layer) => {
      const entry = vectorLayers.get(String(layer.id))
      if (!entry) {
        return
      }

      entry.controller?.abort()
      const controller = new AbortController()
      entry.controller = controller

      loadVectorFeatureCollection(layer, map.getBounds().toBBoxString(), controller.signal)
        .then((data) => {
          if (controller.signal.aborted) {
            return
          }
          entry.overlay.clearLayers()
          entry.overlay.addData(data)
        })
        .catch((error) => {
          if (error.name !== 'AbortError') {
            console.warn('Could not load map layer', layer.name, error)
          }
        })
    }

    const addOverlay = (layer) => {
      if (mode !== 'wms' && isVectorLayer(layer)) {
        const overlay = createVectorOverlay(map, layer)
        vectorLayers.set(String(layer.id), { overlay, controller: null })
        refreshVectorLayer(layer)
        return overlay
      }
      return createWmsOverlay(map, layer)
    }

    const removeOverlay = (layer, overlay) => {
      map.removeLayer(overlay)
      const entry = vectorLayers.get(String(layer.id))
      if (entry) {
        entry.controller?.abort()
        vectorLayers.delete(String(layer.id))
      }
    }

    let refreshTimer = null
    const scheduleRefresh = () => {
      if (!vectorLayers.size) {
        return
      }
      window.clearTimeout(refreshTimer)
      refreshTimer = window.setTimeout(() => {
        vectorLayers.forEach((entry, id) => refreshVectorLayer(layersById.get(id)))
      }, REFRESH_DELAY)
    }
    map.on('moveend', scheduleRefresh)

    checkboxes.forEach((checkbox) => {
      const layer = layersById.get(checkbox.value)
      if (!layer) {
        return
      }

      if (checkbox.checked) {
        overlays.set(String(layer.id), addOverlay(layer))
      }

      checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
          overlays.set(String(layer.id), addOverlay(layer))
        } else {
          const overlay = overlays.get(String(layer.id))
          if (overlay) {
            removeOverlay(layer, overlay)
            overlays.delete(String(layer.id))
          }
        }
        if (status) {
          status.textContent = checkbox.checked
            ? django.gettext('Map layer added')
            : django.gettext('Map layer removed')
        }
      })
    })
  })
}

document.addEventListener('DOMContentLoaded', init, false)
