import React, { useEffect } from 'react'
import { useSearchParams } from 'react-router'
import { ControlBar } from '../ControlBar'
import { CardList } from '../card/CardList'
import { useFetchedItems } from '../contexts/FetchItemsProvider'
import { MapWithMarkers } from './Map'
import { useMediaQuery } from 'react-responsive'

/**
 * Component that displays a list or map view based on the selected mode. It
 * needs to be used in conjunction with the `FetchItemsProvider` component.
 * @param {Object} map - props that are passed to the Map component.
 * @param {string} listStr - accessible text for the list
 */
export const ListMapView = ({ map, listStr, mode, desktopMode }) => {
  const [queryParams, setQueryParams] = useSearchParams()
  const { results } = useFetchedItems()
  const viewMode = queryParams.get('mode') || mode || 'list'
  const desktopViewMode = queryParams.get('desktopMode') || 'map'

  // Responsive Hook
  const isDesktop = useMediaQuery({ minWidth: 768 })

  // Sets the mode to "map" if it's a desktop and no mode is set
  useEffect(() => {
    if (isDesktop && !queryParams.get('page_size')) {
      const newSearchParams = new URLSearchParams(queryParams.toString())
      newSearchParams.set('page_size', '8')
      setQueryParams(newSearchParams, { replace: true })
    }
  }, [isDesktop, queryParams, setQueryParams])

  // Function to toggle map mode
  const handleToggle = () => {
    const newSearchParams = new URLSearchParams(queryParams.toString())
    if (desktopViewMode === 'map') {
      newSearchParams.set('desktopMode', 'list')
    } else {
      newSearchParams.set('desktopMode', 'map')
    }
    setQueryParams(newSearchParams, { replace: true })
  }

  if (!results || !results.map || !results.list) {
    return (
      <>
        <div className="block block--halfgap" />
        <div>Loading...</div>
      </>
    )
  }

  // Desktop: Always both views
  if (isDesktop) {
    return (
      <>
        <div className="block block--halfgap">
          <ControlBar
            mapListViewMode={viewMode}
            showViewModeSwitch={false}
            desktopViewMode={desktopViewMode}
            handleToggle={handleToggle}
          />
        </div>
        <div className="desktop-combined-view">
          {desktopViewMode === 'map' && (
            <div className="map-section">
              <MapWithMarkers
                {...map}
                points={results.map.results.map(f => ({ ...f.point, properties: f }))}
                className="map--list"
                id="map-list"
              />
            </div>
          )}
          <div className="list-section">
            <CardList data={results.list} listStr={listStr} />
          </div>
        </div>
      </>
    )
  }

  // Mobile: Switch as before
  const switchDisplays = () => {
    if (viewMode === 'map') {
      // If results are not jet loaded show a loading message and wait to prevent JS Errors
      if (!results.map || !results.map.results) {
        return <div>Loading map...</div>
      }
      return (
        <MapWithMarkers
          {...map}
          points={results.map.results.map(f => ({ ...f.point, properties: f }))}
          className="map--list"
          id="map-list"
        />
      )
    } else {
      return <CardList data={results.list} listStr={listStr} />
    }
  }

  return (
    <>
      <div className="block block--halfgap">
        <ControlBar mapListViewMode={viewMode} />
      </div>
      {switchDisplays()}
    </>
  )
}
