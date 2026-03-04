import React from 'react'
import { render, screen } from '@testing-library/react'

import ProjectsMap from '../ProjectsMap'

jest.mock('../../contrib/map/Map', () => ({
  Map: ({ children }) => <div data-testid="base-map">{children}</div>
}))

jest.mock('react-leaflet', () => ({
  Circle: ({ style, ...rest }) => <div data-testid="circle" {...rest} />,
  GeoJSON: ({ style, ...rest }) => <div data-testid="geojson" {...rest} />,
  ZoomControl: () => <div>ZoomControl</div>,
  useMap: () => ({
    fitBounds: jest.fn()
  })
}))

jest.mock('adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer', () => ({
  __esModule: true,
  default: ({ children }) => <div>MarkerClusterLayer<div>{children}</div></div>
}))

jest.mock('adhocracy4/adhocracy4/maps_react/static/a4maps_react/ControlWrapper', () => ({
  __esModule: true,
  default: ({ children }) => <div>ControlWrapper<div>{children}</div></div>
}))

jest.mock('adhocracy4', () => ({
  SearchAndShowAddress: () => <div>SearchAndShowAddress</div>
}))

jest.mock('../ProjectsMapInfo', () => ({
  __esModule: true,
  default: () => <div>ProjectsMapInfo</div>
}))

jest.mock('../ProjectTile', () => ({
  __esModule: true,
  default: () => <div>ProjectTile</div>
}))

jest.mock('../ProjectMarker', () => ({
  __esModule: true,
  default: () => <div>ProjectMarker</div>
}))

describe('ProjectsMap overlays', () => {
  const defaultProps = {
    items: [],
    topicChoices: [],
    bounds: [],
    baseUrl: '',
    attribution: '',
    mapboxToken: '',
    omtToken: '',
    useVectorMap: 0
  }

  test('does not render overlays when no districts or kiezradars are active', () => {
    render(
      <ProjectsMap
        {...defaultProps}
        districtPolygons={[]}
        activeDistricts={[]}
        kiezradars={[]}
        activeKiezradars={[]}
      />
    )

    expect(screen.queryByTestId('geojson')).toBeNull()
    expect(screen.queryByTestId('circle')).toBeNull()
  })

  test('renders district polygon and kiezradar circle for active filters', () => {
    const districtPolygons = [
      {
        name: 'Mitte',
        polygon: {
          type: 'FeatureCollection',
          features: []
        }
      }
    ]

    const kiezradars = [
      {
        id: 1,
        name: 'Mein Kiez',
        radius: 1000,
        point: {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [13.4, 52.5]
          }
        }
      }
    ]

    render(
      <ProjectsMap
        {...defaultProps}
        districtPolygons={districtPolygons}
        activeDistricts={['Mitte']}
        kiezradars={kiezradars}
        activeKiezradars={['Mein Kiez']}
      />
    )

    expect(screen.getAllByTestId('geojson')).toHaveLength(1)
    expect(screen.getAllByTestId('circle')).toHaveLength(1)
  })
})
