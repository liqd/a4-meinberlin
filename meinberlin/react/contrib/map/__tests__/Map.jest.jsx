import React from 'react'
import { render, screen } from '@testing-library/react'

import { Map, MapWithMarkers } from '../Map'
jest.mock('adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer', () => ({
  __esModule: true,
  default: (props) => <div>MarkerClusterLayer <div>{props.children}</div></div>
}))
jest.mock('adhocracy4/adhocracy4/maps_react/static/a4maps_react/GeoJsonMarker', () => ({
  __esModule: true,
  default: () => <div>Marker</div>
}))

jest.mock('../ShowMyLocationControl', () => ({
  ShowMyLocationControl: () => <div data-testid="show-my-location-control" />
}))

describe('Map component', () => {
  test('renders Map component with title', () => {
    render(<Map id="test-id" title="Test Title" />)
    expect(screen.getByText('Test Title')).toBeTruthy()
    expect(screen.getByTestId('show-my-location-control')).toBeTruthy()
  })

  test('renders Map component and throws an error when no id is provided', () => {
    expect(() => {
      render(<Map title="Test Title" />)
    }).toThrow('id must be defined when using Map')
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
    expect(screen.getByTestId('show-my-location-control')).toBeTruthy()
  })

  test('renders MapWithMarkers correctly without cluster layer', () => {
    render(<MapWithMarkers id="test-id" points={[points[0]]} />)
    expect(screen.queryByText('MarkerClusterLayer')).toBeFalsy()
    expect(screen.getAllByText('Marker')).toHaveLength(1)
  })
})
