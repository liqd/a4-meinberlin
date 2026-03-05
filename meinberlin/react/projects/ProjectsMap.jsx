import React, {
  useEffect,
  useMemo,
  useCallback,
  useRef,
  forwardRef,
  useImperativeHandle
} from 'react'
import { Circle, GeoJSON, ZoomControl, useMap } from 'react-leaflet'
import * as turf from '@turf/turf'
import MarkerClusterLayer
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer'
import ControlWrapper
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/ControlWrapper'
import { SearchAndShowAddress } from 'adhocracy4'

import { Map } from '../contrib/map/Map'
import ProjectTile from './ProjectTile'
import ProjectMarker from './ProjectMarker'
import ProjectsMapInfo from './ProjectsMapInfo'

const FitToSelection = ({ selectionBbox }) => {
  const map = useMap()

  useEffect(() => {
    if (!map || !selectionBbox) {
      return
    }

    const [minX, minY, maxX, maxY] = selectionBbox
    const southWest = [minY, minX]
    const northEast = [maxY, maxX]

    map.fitBounds([southWest, northEast], { padding: [40, 40] })
  }, [map, selectionBbox])
}

// Component to handle map events and visibility tracking
const MapEventHandler = ({ items, onVisibleMarkersChange }) => {
  const map = useMap()

  const updateVisibleMarkers = useCallback(() => {
    if (!map || !onVisibleMarkersChange) return

    const bounds = map.getBounds()
    const visibleProjects = items.filter(item => {
      if (!item.point) return false
      const { coordinates } = item.point.geometry
      // Leaflet uses [lat, lng] but GeoJSON uses [lng, lat]
      const latLng = { lat: coordinates[1], lng: coordinates[0] }
      return bounds.contains(latLng)
    })

    onVisibleMarkersChange(visibleProjects)
  }, [map, items, onVisibleMarkersChange])

  useEffect(() => {
    if (!map) return

    // Initial update
    updateVisibleMarkers()

    // Update on map movements
    map.on('moveend', updateVisibleMarkers)
    map.on('zoomend', updateVisibleMarkers)
    map.on('resize', updateVisibleMarkers)

    return () => {
      map.off('moveend', updateVisibleMarkers)
      map.off('zoomend', updateVisibleMarkers)
      map.off('resize', updateVisibleMarkers)
    }
  }, [map, updateVisibleMarkers])

  // Also update when items change (filters applied)
  useEffect(() => {
    updateVisibleMarkers()
  }, [items, updateVisibleMarkers])

  return null
}

const Markers = ({ items, topicChoices, onVisibleMarkersChange }) => {
  const [activeProject, setActiveProject] = React.useState(null)

  useEffect(() => {
    // used to preload active marker to prevent flickering
    const img = new Image()
    img.src = '/static/images/map_pin_active.svg'
  }, [])

  const markers = useMemo(() => (
    items
      .filter(item => !!item.point)
      .map(item => ({ ...item.point, properties: item }))
      .map((project) => (
        <ProjectMarker
          key={project.properties.id || project.properties.title}
          topicChoices={topicChoices}
          project={project}
          onOpen={() => setActiveProject(project)}
          onClose={() => setActiveProject(null)}
        />
      ))
  ), [items, topicChoices])

  return (
    <>
      <MarkerClusterLayer>
        {markers}
      </MarkerClusterLayer>
      {activeProject?.properties && (
        <ControlWrapper position="bottomleft" className="project-overlay-control">
          <ProjectTile
            project={activeProject.properties}
            topicChoices={topicChoices}
            ref={(node) => node?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' })}
            isHorizontal
            isMapTile
          />
        </ControlWrapper>
      )}
      <MapEventHandler
        items={items}
        onVisibleMarkersChange={onVisibleMarkersChange}
      />
    </>
  )
}

const ProjectsMap = forwardRef(({
  items,
  topicChoices,
  districtPolygons = [],
  activeDistricts = [],
  kiezradars = [],
  activeKiezradars = [],
  onVisibleMarkersChange,
  bounds,
  ...props
}, ref) => {
  const mapRef = useRef(null)

  useImperativeHandle(ref, () => ({
    setView: (newBounds) => {
      if (mapRef.current && newBounds) {
        mapRef.current.fitBounds(newBounds)
      }
    }
  }))

  useEffect(() => {
    // Debug logging for district and kiezradar overlays
    // eslint-disable-next-line no-console
    console.log('[Kiezradar][ProjectsMap] filters changed', {
      activeDistricts,
      activeKiezradars,
      districtPolygonsCount: districtPolygons?.length ?? 0,
      kiezradarsCount: kiezradars?.length ?? 0
    })
  }, [activeDistricts, activeKiezradars, districtPolygons, kiezradars])

  const activeDistrictFeatures = useMemo(
    () => {
      if (!districtPolygons || !activeDistricts || activeDistricts.length === 0) {
        return []
      }

      const normalise = (value) => (
        (value || '').toString().toLowerCase().trim()
      )

      const activeSet = new Set(activeDistricts.map(normalise))

      return districtPolygons.filter((district) => (
        activeSet.has(normalise(district.name))
      ))
    },
    [districtPolygons, activeDistricts]
  )

  const activeKiezradarFeatures = useMemo(
    () => {
      if (!kiezradars || !activeKiezradars || activeKiezradars.length === 0) {
        return []
      }

      const activeSet = new Set(activeKiezradars)

      return kiezradars.filter((kiez) => (
        activeSet.has(kiez.name) &&
        kiez.point &&
        kiez.point.geometry &&
        Array.isArray(kiez.point.geometry.coordinates)
      ))
    },
    [kiezradars, activeKiezradars]
  )

  const { greyedOutArea, selectionBbox } = useMemo(
    () => {
      if (activeDistrictFeatures.length === 0 && activeKiezradarFeatures.length === 0) {
        // eslint-disable-next-line no-console
        console.log('[Kiezradar][ProjectsMap] no active districts, skipping mask')
        return { greyedOutArea: null, selectionBbox: null }
      }

      const selectedDistrictFeatures = activeDistrictFeatures
        .flatMap((district) => (district.polygon && district.polygon.features) || [])

      const selectedKiezFeatures = activeKiezradarFeatures.map((kiez) =>
        turf.buffer(kiez.point, kiez.radius, { units: 'meters' })
      )

      const selectedFeatures = [...selectedDistrictFeatures, ...selectedKiezFeatures]

      if (selectedFeatures.length === 0) {
        // eslint-disable-next-line no-console
        console.log('[Kiezradar][ProjectsMap] active selection without features', {
          activeDistrictFeatures,
          activeKiezradarFeatures
        })
        return { greyedOutArea: null, selectionBbox: null }
      }

      try {
        const selectionCollection = {
          type: 'FeatureCollection',
          features: selectedFeatures
        }

        // Bounding box für Auto-Zoom berechnen
        const selectionBbox = turf.bbox(selectionCollection)

        // Maske: Welt minus alle ausgewählten Bezirke (per sequentieller Differenz),
        // damit mehrere Bezirke gleichzeitig freigestellt werden.
        const worldFeature = turf.bboxPolygon([-180, -90, 180, 90])
        let mask = worldFeature

        selectedFeatures.forEach((feature, index) => {
          try {
            const nextMask = turf.difference(mask, feature)

            if (!nextMask) {
              // eslint-disable-next-line no-console
              console.log('[Kiezradar][ProjectsMap] mask difference returned null for feature', {
                index,
                featureBbox: turf.bbox(feature)
              })
              return
            }

            mask = nextMask
          } catch (e) {
            // eslint-disable-next-line no-console
            console.error('[Kiezradar][ProjectsMap] error while subtracting feature from mask', {
              index,
              error: e
            })
          }
        })

        if (mask === worldFeature) {
          return { greyedOutArea: null, selectionBbox }
        }

        // eslint-disable-next-line no-console
        console.log('[Kiezradar][ProjectsMap] mask computed', {
          selectionBbox,
          featureCount: selectedFeatures.length
        })

        return {
          greyedOutArea: {
            type: 'FeatureCollection',
            features: [mask]
          },
          selectionBbox
        }
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error('[Kiezradar][ProjectsMap] error while computing mask', e)
        return { greyedOutArea: null, selectionBbox: null }
      }
    },
    [activeDistrictFeatures, activeKiezradarFeatures]
  )

  const maskKey = useMemo(
    () => (
      (activeDistricts && activeDistricts.length > 0) || (activeKiezradars && activeKiezradars.length > 0)
        ? `grey-mask-${[...activeDistricts].sort().join('-')}--${[...activeKiezradars].sort().join('-')}`
        : 'grey-mask-none'
    ),
    [activeDistricts, activeKiezradars]
  )
  return (
    <div className="projects-map">
      <ProjectsMapInfo className="projects-map-info--mobile" />
      <div
        id="map-live-region"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {/* Screen reader announcements will go here */}
      </div>
      <Map
        ref={mapRef}
        zoomControl={false}
        maxZoom={18}
        bounds={bounds}
        {...props}
        id="project-map"
        key="project-map"
        style={{ minHeight: '100%', height: '100%' }}
        className="projects-map__map"
      >
        <FitToSelection selectionBbox={selectionBbox} />
        <SearchAndShowAddress apiUrl="/api/geodata/search" />
        <ControlWrapper position="bottomleft" className="projects-map-info__wrapper">
          <ProjectsMapInfo />
        </ControlWrapper>
        <ZoomControl position="topleft" />
        {greyedOutArea && (
          <GeoJSON
            key={maskKey}
            data={greyedOutArea}
            style={() => ({
              color: '#000000',
              weight: 0,
              fill: true,
              fillColor: '#000000',
              fillOpacity: 0.4
            })}
          />
        )}
        {activeDistrictFeatures.map((district) => (
          <GeoJSON
            key={`district-${district.name}`}
            data={district.polygon}
            style={() => ({
              color: '#000000',
              weight: 1,
              fill: false
            })}
          />
        ))}
        {activeKiezradarFeatures.map((kiez) => {
          const [lng, lat] = kiez.point.geometry.coordinates
          return (
            <Circle
              key={`kiez-${kiez.id || kiez.name}`}
              center={[lat, lng]}
              radius={kiez.radius}
              pathOptions={{ color: '#000000', weight: 1, fillOpacity: 0.1 }}
            />
          )
        })}
        <Markers
          items={items}
          topicChoices={topicChoices}
          onVisibleMarkersChange={onVisibleMarkersChange}
        />
      </Map>
    </div>
  )
})

ProjectsMap.displayName = 'ProjectsMap'
export default ProjectsMap
