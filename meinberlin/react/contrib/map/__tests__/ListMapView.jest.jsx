import React from 'react'
import { render, screen } from '@testing-library/react'
import { ListMapView } from '../ListMapView'
import { useSearchParams } from 'react-router-dom'
import { useFetchedItems } from '../../contexts/FetchItemsProvider'

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useSearchParams: jest.fn()
}))

jest.mock('../../card/CardList', () => ({
  CardList: () => <div>CardList</div>
}))

jest.mock('../Map', () => ({
  MapWithMarkers: () => <div>MapWithMarkers</div>
}))

jest.mock('../../contexts/FetchItemsProvider', () => ({
  useFetchedItems: jest.fn()
}))

describe('ListMapView', () => {
  let mockResults

  beforeEach(() => {
    mockResults = {
      map: {
        results: []
      },
      list: {
        results: [],
        permissions: {
          view_comment_count: true,
          view_rate_count: true
        }
      }
    }

    // eslint-disable-next-line n/no-unsupported-features/node-builtins
    useSearchParams.mockImplementation(() => [new URLSearchParams()])
    useFetchedItems.mockImplementation(() => ({ results: mockResults }))
  })

  it('renders list mode by default', () => {
    render(<ListMapView map={{}} />)
    expect(screen.getByText('CardList')).toBeTruthy()
    expect(screen.queryByText('MapWithMarkers')).toBeFalsy()
  })

  it('renders list mode when set in url', () => {
    // eslint-disable-next-line n/no-unsupported-features/node-builtins
    useSearchParams.mockImplementation(() => [new URLSearchParams({ mode: 'list' })])
    render(<ListMapView map={{}} />)
    expect(screen.getByText('CardList')).toBeTruthy()
    expect(screen.queryByText('MapWithMarkers')).toBeFalsy()
  })

  it('renders map when set in url', () => {
    // eslint-disable-next-line n/no-unsupported-features/node-builtins
    useSearchParams.mockImplementation(() => [new URLSearchParams({ mode: 'map' })])
    render(<ListMapView map={{}} />)
    expect(screen.queryByText('CardList')).toBeFalsy()
    expect(screen.getByText('MapWithMarkers')).toBeTruthy()
  })
})
