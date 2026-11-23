import React from 'react'
import { render, screen } from '@testing-library/react'

import { Map, MapWithMarkers } from '../Map'

jest.mock('react-leaflet', () => {
  const React = require('react')
  return {
    ...jest.requireActual('react-leaflet'),
    WMSTileLayer: (props) => React.createElement('div', {
      'data-testid': 'wms-layer',
      'data-url': props.url,
      'data-layers': props.layers
    })
  }
})
jest.mock('adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer', () => ({
  __esModule: true,
  default: (props) => <div>MarkerClusterLayer <div>{props.children}</div></div>
}))
jest.mock('adhocracy4/adhocracy4/maps_react/static/a4maps_react/GeoJsonMarker', () => ({
  __esModule: true,
  default: () => <div>Marker</div>
}))

describe('Map component', () => {
  test('renders Map component with title', () => {
    render(<Map id="test-id" title="Test Title" />)
    expect(screen.getByText('Test Title')).toBeTruthy()
  })

  test('renders Map component and throws an error when no id is provided', () => {
    expect(() => {
      render(<Map title="Test Title" />)
    }).toThrow('id must be defined when using Map')
  })

  test('renders the selected WMS layer and its name', () => {
    render(
      <Map
        id="test-id"
        layer={{
          url: 'https://gdi.berlin.de/services/wms/baumbestand',
          layers: 'strassenbaeume',
          title: 'Straßenbäume',
          attribution: 'GDI Berlin'
        }}
      />
    )
    expect(screen.getByTestId('wms-layer').getAttribute('data-layers')).toBe(
      'strassenbaeume'
    )
    expect(
      screen.getByTestId('wms-layer').getAttribute('data-url')
    ).toBe('https://gdi.berlin.de/services/wms/baumbestand')
    expect(screen.getByText(/Straßenbäume/)).toBeTruthy()
  })

  test('renders no WMS layer when no layer is selected', () => {
    render(<Map id="test-id" />)
    expect(screen.queryByTestId('wms-layer')).toBeNull()
    expect(screen.queryByText(/Straßenbäume/)).toBeNull()
  })
})

describe('MapWithMarkers component', () => {
  const points = [{
    id: '1',
    geometry: {
      coordinates: [123.456, 78.910]
    },
    properties: {}
  }, {
    id: '2',
    geometry: {
      coordinates: [1112.1314, 15.1617]
    },
    properties: {}
  }]

  test('renders MapWithMarkers with cluster', () => {
    render(<MapWithMarkers id="test-id" points={points} />)
    expect(screen.getByText('MarkerClusterLayer')).toBeTruthy()
    expect(screen.getAllByText('Marker')).toHaveLength(2)
  })

  test('renders MapWithMarkers correctly without cluster layer', () => {
    render(<MapWithMarkers id="test-id" points={[points[0]]} />)
    expect(screen.queryByText('MarkerClusterLayer')).toBeFalsy()
    expect(screen.getAllByText('Marker')).toHaveLength(1)
  })
})
