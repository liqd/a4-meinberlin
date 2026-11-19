import React from 'react'
import L from 'leaflet'
import { ShowMyLocationControl as A4ShowMyLocationControl } from 'adhocracy4'

// Berlin and Brandenburg. Positions outside this area must not move the map
// to a place without any projects.
export const DEFAULT_AREA_BOUNDS = [[51.2, 11.0], [53.7, 15.0]]

const locationIcon = L.icon({
  iconUrl: '/static/images/map_pin_location.svg',
  iconSize: [36, 48],
  iconAnchor: [18, 48],
  className: 'show-my-location__marker'
})

/**
 * meinBerlin configuration for the reusable adhocracy4 location control.
 */
export const ShowMyLocationControl = (props) => (
  <A4ShowMyLocationControl
    areaBounds={DEFAULT_AREA_BOUNDS}
    icon={locationIcon}
    {...props}
  />
)

export default ShowMyLocationControl
