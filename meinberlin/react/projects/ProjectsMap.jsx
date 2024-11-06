import React from 'react'
import { Popup } from 'react-leaflet'
import MarkerClusterLayer
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer'
import GeoJsonMarker
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/GeoJsonMarker'

import { Map } from '../contrib/map/Map'
import ProjectMapOverlay from './ProjectMapOverlay'
import ProjectTile from './ProjectTile'

const Markers = React.memo(({ items, topicChoices }) => {
  const [activeProject, setActiveProject] = React.useState(null)

  return (
    <>
      <MarkerClusterLayer>
        {items
          .filter(item => !!item.point)
          .map(item => ({ ...item.point, properties: item }))
          .map((project) => (
            <GeoJsonMarker
              key={project.properties.title}
              feature={project}
              eventHandlers={{
                popupopen: () => setActiveProject(project),
                popupclose: () => setActiveProject(null)
              }}
            >
              <Popup
                className="projects-map__popup"
                offset={[0, 270]}
                maxWidth={400}
                minWidth={400}
              >
                <ProjectTile
                  project={project.properties}
                  isHorizontal
                  topicChoices={topicChoices}
                  isMapTile
                />
              </Popup>
            </GeoJsonMarker>
          ))}
      </MarkerClusterLayer>
      <ProjectMapOverlay position="bottomleft" project={activeProject?.properties} topicChoices={topicChoices} />
    </>
  )
})
Markers.displayName = 'Markers'

const ProjectsMap = ({ items, topicChoices, ...props }) => {
  return (
    <div className="projects-map">
      <Map
        scrollWheelZoom={false}
        zoomControl
        maxZoom={18}
        {...props}
        id="project-map"
        key="project-map"
        style={{ minHeight: '100%', height: '100%' }}
        className="projects-map__map"
      >
        <Markers items={items} topicChoices={topicChoices} />
      </Map>
    </div>
  )
}

export default ProjectsMap
