import django from 'django'
import L from 'leaflet'

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

const toggleLayer = (map, layer, overlays, show) => {
  const id = String(layer.id)
  const existing = overlays.get(id)

  if (show && !existing) {
    const overlay = L.tileLayer.wms(layer.url, {
      layers: layer.layer,
      format: 'image/png',
      transparent: true,
      opacity: layer.opacity,
      attribution: layer.attribution,
      className: 'map-layer-overlay'
    })
    overlay.addTo(map)
    overlays.set(id, overlay)
  } else if (!show && existing) {
    map.removeLayer(existing)
    overlays.delete(id)
  }
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

    const layersById = new Map(
      layers.map((layer) => [String(layer.id), layer])
    )
    const form = element.closest('form')
    const checkboxes = form
      ? form.querySelectorAll('input[name="layers"]')
      : []
    const status = form
      ? form.querySelector('[data-map-layer-status]')
      : null
    const overlays = new Map()

    checkboxes.forEach((checkbox) => {
      const layer = layersById.get(checkbox.value)
      if (!layer) {
        return
      }

      toggleLayer(map, layer, overlays, checkbox.checked)

      checkbox.addEventListener('change', () => {
        toggleLayer(map, layer, overlays, checkbox.checked)
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
