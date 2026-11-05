import React from 'react'
import django from 'django'
import { GeoJSON, WMSTileLayer, useMap } from 'react-leaflet'
import BaseMap from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/Map'
import MarkerClusterLayer
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer'
import GeoJsonMarker
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/GeoJsonMarker'
import {
  getLayerMode,
  isVectorLayer,
  loadVectorFeatureCollection,
  vectorStyle
} from '../../../assets/js/map_layers_vector'
import { ItemPopup } from './ItemPopup'

const translations = {
  beginningMap: django.gettext('A map representation follows.'),
  endMap: django.gettext('End of map.'),
  skipMap: django.gettext('Skip map')
}

const VectorLayer = ({ layer }) => {
  const map = useMap()
  const [data, setData] = React.useState(null)

  React.useEffect(() => {
    let controller = null

    const load = () => {
      controller?.abort()
      controller = new AbortController()
      loadVectorFeatureCollection(layer, map.getBounds().toBBoxString(), controller.signal)
        .then((collection) => {
          if (!controller.signal.aborted) {
            setData(collection)
          }
        })
        .catch((error) => {
          if (error.name !== 'AbortError') {
            console.warn('Could not load map layer', layer.name, error)
          }
        })
    }

    load()
    map.on('moveend', load)

    return () => {
      controller?.abort()
      map.off('moveend', load)
    }
  }, [map, layer.id])

  if (!data) {
    return null
  }

  return (
    <GeoJSON
      data={data}
      style={(feature) => vectorStyle(layer, feature)}
      className="map-layer-overlay"
    />
  )
}

const MapLayerOverlays = ({ layers = [] }) => {
  const mode = getLayerMode()

  return (
    <>
      {layers.map((layer) => (
        mode !== 'wms' && isVectorLayer(layer)
          ? <VectorLayer key={layer.id || layer.wfsUrl} layer={layer} />
          : <WMSTileLayer
              key={layer.id || layer.url + layer.layer}
              url={layer.url}
              layers={layer.layer}
              format="image/png"
              transparent
              opacity={layer.opacity ?? 0.7}
              attribution={layer.attribution}
              className="map-layer-overlay"
            />
      ))}
    </>
  )
}

/**
 * Creates a Map component.
 *
 * @param {object} props - The properties for the Map component.
 * @param {string} props.id - The unique identifier for the Map component.
 * @param {string} props.title - The title for the Map component.
 * @param {Array<object>} props.layers - Optional WMS overlays.
 * @returns {React.Element} - The rendered Map component.
 * @throws {Error} - If id is not defined.
 */
export const Map = React.forwardRef(
  function Map ({ id, title, layers, children, ...props }, ref) {
    if (!id) {
      throw new Error('id must be defined when using Map')
    }

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
              <MapLayerOverlays layers={layers} />
              {children}
            </BaseMap>
          </div>
        </div>

        <div id={id + '_skipmap'}>
          <p className="aural">{translations.endMap}</p>
        </div>
      </div>
    )
  }
)

/**
 * Represents a map component with markers.
 *
 * @param {object} props - The properties to pass to the Map component.
 * @param {Array<object>} points - The array of points to create markers from.
 * @param {boolean} withoutPopup - Indicates whether to exclude the popup for each marker.
 * @param {ReactNode} children - Any additional controls etc. to be added to the map
 * @returns {JSX.Element} - The rendered map component with markers.
 */
export const MapWithMarkers = ({ points, withoutPopup, children, ...props }) => {
  const markers = points.map((feature, index) => (
    <GeoJsonMarker key={index} feature={feature}>
      {!withoutPopup && <ItemPopup feature={feature} />}
    </GeoJsonMarker>
  ))
  return (
    <Map
      {...props}
    >
      {points.length > 1 ? <MarkerClusterLayer>{markers}</MarkerClusterLayer> : markers}
      {children}
    </Map>
  )
}
