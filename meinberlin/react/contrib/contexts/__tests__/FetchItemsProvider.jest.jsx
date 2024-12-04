import React from 'react'
import { screen, render, waitFor } from '@testing-library/react'
import { FetchItemsProvider, useFetchedItems } from '../FetchItemsProvider'

const TestComponent = () => {
  const { results, currentPage, isMapAndList } = useFetchedItems()

  return (
    <div>
      <div data-testid="results">{JSON.stringify(results)}</div>
      <div data-testid="currentPage">{currentPage}</div>
      <div data-testid="isMapAndList">{isMapAndList.toString()}</div>
    </div>
  )
}

// Mock the global fetch function
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve('1234')
  })
)

// Mock react-router-dom hooks
jest.mock('react-router', () => ({
  ...jest.requireActual('react-router'),
  useLocation: jest.fn().mockReturnValue({ search: '?mode=list&page=1' }),
  useSearchParams: jest.fn().mockReturnValue([{ get: jest.fn((key) => ({ mode: 'list', page: '1' }[key])) }])
}))

// Mock react-router-dom hooks
jest.mock('../../Spinner', () => ({
  __esModule: true,
  default: () => <div data-testid="spinner" />
}))

// Mock requestIdleCallback
global.requestIdleCallback = jest.fn().mockImplementation((cb) => setTimeout(cb, 0))

describe('FetchItemsProvider', () => {
  it('fetches data and provides it via context', async () => {
    render(
      <FetchItemsProvider apiUrl="/api/items" isMapAndList>
        <TestComponent />
      </FetchItemsProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('results').textContent).toEqual('{"list":"1234","map":"1234"}')
      expect(screen.getByTestId('currentPage').textContent).toEqual('1')
      expect(screen.getByTestId('isMapAndList').textContent).toEqual('true')
    })
  })

  it('displays spinner initially', async () => {
    render(
      <FetchItemsProvider apiUrl="/api/items" isMapAndList>
        <TestComponent />
      </FetchItemsProvider>
    )

    expect(screen.getByTestId('spinner')).toBeTruthy()
  })
})
