// Shared helpers to render map layers as vector features (GeoJSON from WFS).

const COLOR_RULES = [
  [/wohn/, '#c0392b'],
  [/gemischt|misch/, '#8c6d31'],
  [/gewerbe|industrie/, '#756bb1'],
  [/gruen|grün|freif/, '#31a354'],
  [/wald|forst/, '#006d2c'],
  [/wasser/, '#2c7fb8'],
  [/verkehr|strasse|straße|bahn/, '#636363'],
  [/sonder/, '#e6550d']
]

const FALLBACK_COLORS = [
  '#1f78b4',
  '#33a02c',
  '#e31a1c',
  '#ff7f00',
  '#6a3d9a',
  '#b15928',
  '#a6cee3',
  '#fb9a99'
]

const fallbackColor = (value) => {
  let hash = 0
  for (let i = 0; i < value.length; i++) {
    hash = (hash * 31 + value.charCodeAt(i)) % 9973
  }
  return FALLBACK_COLORS[hash % FALLBACK_COLORS.length]
}

/**
 * Returns the render mode requested via the URL, "vector" by default.
 * Use ?map_layers=wms to compare with the raster (WMS) rendering.
 */
export const getLayerMode = () => {
  const params = new URLSearchParams(window.location.search)
  return params.get('map_layers') === 'wms' ? 'wms' : 'vector'
}

export const isVectorLayer = (layer) => Boolean(layer && layer.wfsUrl && layer.wfsLayer)

export const wfsUrlFor = (layer, bounds) => {
  const params = new URLSearchParams({
    service: 'WFS',
    version: '2.0.0',
    request: 'GetFeature',
    typeNames: layer.wfsLayer,
    outputFormat: 'application/json',
    srsName: 'EPSG:4326'
  })
  if (bounds) {
    params.set('bbox', `${bounds},EPSG:4326`)
  }
  return `${layer.wfsUrl}?${params.toString()}`
}

export const loadVectorFeatureCollection = async (layer, bounds, signal) => {
  const response = await fetch(wfsUrlFor(layer, bounds), { signal })
  if (!response.ok) {
    throw new Error(`WFS request failed with status ${response.status}`)
  }
  return response.json()
}

export const vectorStyle = (layer, feature) => {
  const properties = (feature && feature.properties) || {}
  const value = String(properties[layer.wfsProperty] || '').toLowerCase()
  const rule = COLOR_RULES.find(([pattern]) => pattern.test(value))

  return {
    color: '#555555',
    weight: 1,
    opacity: 0.6,
    fillColor: rule ? rule[1] : fallbackColor(value),
    fillOpacity: 0.55
  }
}
