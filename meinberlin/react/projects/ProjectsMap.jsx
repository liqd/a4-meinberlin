import React, { useEffect, useMemo } from 'react'
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

  return null
}

const Markers = ({ items, topicChoices }) => {
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
          key={project.properties.title}
          topicChoices={topicChoices}
          project={project}
          onOpen={() => setActiveProject(project)}
          onClose={() => setActiveProject(null)}
        />
      ))
  ), [items])

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
    </>
  )
}

const ProjectsMap = ({
  items,
  topicChoices,
  districtPolygons = [],
  activeDistricts = [],
  kiezradars = [],
  activeKiezradars = [],
  ...props
}) => {
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
      if (activeDistrictFeatures.length === 0) {
        // eslint-disable-next-line no-console
        console.log('[Kiezradar][ProjectsMap] no active districts, skipping mask')
        return { greyedOutArea: null, selectionBbox: null }
      }

      const selectedFeatures = activeDistrictFeatures
        .flatMap((district) => (district.polygon && district.polygon.features) || [])

      if (selectedFeatures.length === 0) {
        // eslint-disable-next-line no-console
        console.log('[Kiezradar][ProjectsMap] active districts without features', {
          activeDistrictFeatures
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
    [activeDistrictFeatures]
  )

  const maskKey = useMemo(
    () => (
      activeDistricts && activeDistricts.length > 0
        ? `grey-mask-${[...activeDistricts].sort().join('-')}`
        : 'grey-mask-none'
    ),
    [activeDistricts]
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
        zoomControl={false}
        maxZoom={18}
        {...props}
        id="project-map"
        key="project-map"
        style={{ minHeight: '100%', height: '100%' }}
        className="projects-map__map"
      >
        <FitToSelection selectionBbox={selectionBbox} />
        <SearchAndShowAddress apiUrl="/api/geodata/search" />
        {/* <SearchAndShowAddress apiUrl="https://bplan-prod.liqd.net/api/addresses/" /> */}
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
              pathOptions={{ color: '#00A982', weight: 2, fillOpacity: 0.1 }}
            />
          )
        })}
        <Markers items={items} topicChoices={topicChoices} />
      </Map>
    </div>
  )
}

export default ProjectsMap
