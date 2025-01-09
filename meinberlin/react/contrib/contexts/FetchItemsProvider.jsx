import React, {
  useState,
  useEffect,
  createContext,
  useContext
} from 'react'
import { useLocation, useSearchParams } from 'react-router'
import Spinner from '../Spinner'

const DataContext = createContext()

/**
 * Custom Hook to fetch and return items using Context
 * @returns {Object} The fetched items
 */
export const useFetchedItems = () => {
  // Use the useContext hook to access the DataContext
  return useContext(DataContext)
}

const fetchItems = async (url, urlParams = '') => {
  const response = await fetch(url + urlParams)
  return await response.json()
}

/**
 * A provider component for fetching and managing items data from an API.
 * Wrap this around a component that needs to fetch and manage items data and
 * then use the `useFetchedItems` hook to access the data anywhere in the
 * component tree within the provider.
 *
 * Usage:
 * Use the FetchItemsProvider Component as a wrapper for any component that needs
 * access to fetched items. Provide the necessary props: `apiUrl` (API endpoint),
 * `isMapAndList` (true/false), and `children` (components you want to provide data for)
 *
 * Example:
 *  <FetchItemsProvider apiUrl="/api/items" isMapAndList>
 *    <YourComponent />
 *  </FetchItemsProvider>
 *
 * Then in the child component (`YourComponent` in this case) you can use the
 * `useFetchedItems` hook to get the fetched data.
 *
 * Example:
 *  const YourComponent = () => {
 *    const {results, currentPage, isMapAndList, viewMode} = useFetchedItems();
 *    // Now you have access to `results`, `currentPage`, `viewMode` and `isMapAndList` data
 *    return <div>Your JSX goes here</div>
 *  }
 *
 * @see https://react.dev/learn/passing-data-deeply-with-context
 *
 * @param {string} apiUrl - The URL of the API endpoint.
 * @param {boolean} isMapAndList - Flag indicating whether both map and list views are supported.
 * @param {React.ReactNode} children - The child components to render.
 * @returns {React.ReactNode} - The rendered child components.
 */
export function FetchItemsProvider ({ apiUrl, isMapAndList, children }) {
  const location = useLocation()
  const [queryParams] = useSearchParams()
  const [data, setData] = useState({ list: null, map: null })
  const [currentPage, setCurrentPage] = useState(1)
  const viewMode = queryParams.get('mode') || 'list'
  const value = { results: data, currentPage, viewMode, isMapAndList: !!isMapAndList }

  const fetchAndUpdate = async (url, key) => {
    const params = new URLSearchParams(location.search)
    params.delete('mode')

    if (key === 'map') {
      params.append('page_size', '10000')
      params.delete('page')
    }
    try {
      const json = await fetchItems(url, '?' + params)
      setData(prevData => ({ ...prevData, [key]: json }))
      setCurrentPage(queryParams.get('page') || 1)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    // fetches and updates data from an API. For each view mode ('list', 'map'),
    // it calls fetchAndUpdate directly if it's the current mode, else it sets
    // an idle callback.
    const views = isMapAndList ? ['list', 'map'] : ['list']

    for (const view of views) {
      if (viewMode === view) {
        fetchAndUpdate(apiUrl, view)
      } else {
        if (typeof requestIdleCallback === 'function') {
          requestIdleCallback(() => fetchAndUpdate(apiUrl, view), { timeout: 1000 })
        } else {
          setTimeout(() => fetchAndUpdate(apiUrl, view), 1000)
        }
      }
    }
  }, [apiUrl, location.search])

  if (data[viewMode] === null) {
    return <Spinner />
  }

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  )
}
