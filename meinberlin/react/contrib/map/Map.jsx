import React from 'react'
import django from 'django'
import { WMSTileLayer } from 'react-leaflet'
import BaseMap from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/Map'
import MarkerClusterLayer from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer'
import GeoJsonMarker from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/GeoJsonMarker'
import { ItemPopup } from './ItemPopup'

const translations = {
  beginningMap: django.gettext('A map representation follows.'),
  endMap: django.gettext('End of map.'),
  skipMap: django.gettext('Skip map'),
  mapLayer: django.gettext('Map layer')
}

/**
 * Creates a Map component.
 *
 * @param {object} props - The properties for the Map component.
 * @param {string} props.id - The unique identifier for the Map component.
 * @param {string} props.title - The title for the Map component.
 * @returns {React.Element} - The rendered Map component.
 * @throws {Error} - If id is not defined.
 */
export const Map = React.forwardRef(function Map (
  { id, title, layer, children, ...props },
  ref
) {
  if (!id) {
    throw new Error('id must be defined when using Map')
  }

  const hasLayer = Boolean(layer && layer.url && layer.layers)

  return (
    <div className="modul-geomap" id={id}>
      {title && <h2 className="title">{title}</h2>}
      <div className="geomap-main">
        <p className="skipmap">
          <span className="aural">{translations.beginningMap}</span>
          <a href={'#' + id + '_skipmap'}>{translations.skipMap}</a>
        </p>
        <div className="geomap-container">
          <BaseMap {...props} ref={ref}>
            {hasLayer && (
              <WMSTileLayer
                url={layer.url}
                layers={layer.layers}
                format="image/png"
                transparent
                version="1.3.0"
                attribution={layer.attribution || ''}
                zIndex={1}
              />
            )}
            {children}
          </BaseMap>
          {hasLayer && (
            <p className="geomap__layer-note">
              {translations.mapLayer}: {layer.title || layer.layers}
            </p>
          )}
        </div>
      </div>

      <div id={id + '_skipmap'}>
        <p className="aural">{translations.endMap}</p>
      </div>
    </div>
  )
})

/**
 * Represents a map component with markers.
 *
 * @param {object} props - The properties to pass to the Map component.
 * @param {Array<object>} points - The array of points to create markers from.
 * @param {boolean} withoutPopup - Indicates whether to exclude the popup for each marker.
 * @param {ReactNode} children - Any additional controls etc. to be added to the map
 * @returns {JSX.Element} - The rendered map component with markers.
 */
export const MapWithMarkers = ({
  points,
  withoutPopup,
  children,
  ...props
}) => {
  const markers = points.map((feature, index) => (
    <GeoJsonMarker key={index} feature={feature}>
      {!withoutPopup && <ItemPopup feature={feature} />}
    </GeoJsonMarker>
  ))
  const markerLayer = points.length > 1
    ? <MarkerClusterLayer>{markers}</MarkerClusterLayer>
    : markers

  return (
    <Map {...props}>
      {markerLayer}
      {children}
    </Map>
  )
}
