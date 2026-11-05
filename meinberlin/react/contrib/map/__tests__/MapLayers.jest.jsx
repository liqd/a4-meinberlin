import React from 'react'
import { render, screen } from '@testing-library/react'

import { MapWithMarkers } from '../Map'

jest.mock('react-leaflet', () => ({
  WMSTileLayer: (props) => (
    <div
      data-testid="wms-layer"
      data-layer={props.layers}
      data-classname={props.className}
    />
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

describe('Map layer overlays', () => {
  const layers = [{
    id: 1,
    url: 'https://example.org/wms',
    layer: 'test_layer',
    attribution: '© Test',
    opacity: 0.7
  }]

  test('renders WMS overlays with the non-interactive CSS class', () => {
    render(<MapWithMarkers id="test-id" points={[]} layers={layers} />)

    const overlay = screen.getByTestId('wms-layer')
    expect(overlay.dataset.layer).toBe('test_layer')
    expect(overlay.dataset.classname).toBe('map-layer-overlay')
  })

  test('renders no overlays without layers', () => {
    render(<MapWithMarkers id="test-id" points={[]} />)

    expect(screen.queryByTestId('wms-layer')).toBeNull()
  })
})
