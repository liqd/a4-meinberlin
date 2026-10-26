import React from 'react'
import { render, screen } from '@testing-library/react'

import { MapWithMarkers } from '../Map'
import { getLayerMode, wfsUrlFor } from '../../../../assets/js/map_layers_vector'

jest.mock('react-leaflet', () => ({
  WMSTileLayer: (props) => (
    <div data-testid="wms-layer" data-layer={props.layers} />
  ),
  GeoJSON: (props) => (
    <div
      data-testid="geojson-layer"
      data-features={props.data ? props.data.features.length : 0}
      data-classname={props.className}
    />
  ),
  useMap: () => ({
    getBounds: () => ({ toBBoxString: () => '13.3,52.4,13.5,52.6' }),
    on: jest.fn(),
    off: jest.fn()
  })
}))
jest.mock('adhocracy4/adhocracy4/maps_react/static/a4maps_react/Map', () => ({
  __esModule: true,
  default: (props) => <div>{props.children}</div>
}))
jest.mock(
  'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer',
  () => ({
    __esModule: true,
    default: (props) => <div>{props.children}</div>
  })
)
jest.mock('adhocracy4/adhocracy4/maps_react/static/a4maps_react/GeoJsonMarker', () => ({
  __esModule: true,
  default: (props) => <div>{props.children}</div>
}))

const vectorLayer = {
  id: 1,
  name: 'FNP',
  url: 'https://example.org/wms',
  layer: 'test_layer',
  wfsUrl: 'https://example.org/wfs',
  wfsLayer: 'test:layer',
  wfsProperty: 'nutzungsart',
  attribution: '© Test',
  opacity: 0.7
}

describe('Vector map layers', () => {
  beforeEach(() => {
    window.history.pushState({}, '', '/')
    global.fetch = jest.fn(() => Promise.resolve({
      ok: true,
      json: () => Promise.resolve({
        type: 'FeatureCollection',
        features: [{ type: 'Feature', properties: {}, geometry: null }]
      })
    }))
  })

  afterEach(() => {
    jest.clearAllMocks()
    delete global.fetch
  })

  test('requests the WFS endpoint with the current bounds', () => {
    expect(wfsUrlFor(vectorLayer, '13.3,52.4,13.5,52.6')).toBe(
      'https://example.org/wfs?service=WFS&version=2.0.0&request=GetFeature' +
      '&typeNames=test%3Alayer&outputFormat=application%2Fjson' +
      '&srsName=EPSG%3A4326&bbox=13.3%2C52.4%2C13.5%2C52.6%2CEPSG%3A4326'
    )
  })

  test('renders a GeoJSON overlay for layers with a WFS endpoint', async () => {
    render(<MapWithMarkers id="test-id" points={[]} layers={[vectorLayer]} />)

    const overlay = await screen.findByTestId('geojson-layer')
    expect(overlay.dataset.features).toBe('1')
    expect(overlay.dataset.classname).toBe('map-layer-overlay')
    expect(screen.queryByTestId('wms-layer')).toBeNull()
  })

  test('keeps the WMS rendering with ?map_layers=wms', () => {
    window.history.pushState({}, '', '/?map_layers=wms')
    expect(getLayerMode()).toBe('wms')

    render(<MapWithMarkers id="test-id" points={[]} layers={[vectorLayer]} />)

    expect(screen.getByTestId('wms-layer')).toBeTruthy()
    expect(screen.queryByTestId('geojson-layer')).toBeNull()
  })
})
