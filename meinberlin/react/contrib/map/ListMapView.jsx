import React from 'react'
import { useSearchParams } from 'react-router'
import { ControlBar } from '../ControlBar'
import { CardList } from '../card/CardList'
import { useFetchedItems } from '../contexts/FetchItemsProvider'
import { MapWithMarkers } from './Map'

/**
 * Component that displays a list or map view based on the selected mode. It
 * needs to be used in conjunction with the `FetchItemsProvider` component.
 * @param {Object} map - props that are passed to the Map component.
 * @param {string} listStr - accessible text for the list
 */
export const ListMapView = ({ map, listStr, mode }) => {
  const [queryParams] = useSearchParams()
  const { results } = useFetchedItems()
  const viewMode = queryParams.get('mode') || mode || 'list'

  const switchDisplays = () => {
    if (viewMode === 'map') {
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
