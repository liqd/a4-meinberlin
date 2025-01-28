import React, { useEffect, useMemo } from 'react'
import { ZoomControl } from 'react-leaflet'
import MarkerClusterLayer
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MarkerClusterLayer'
import ControlWrapper
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/ControlWrapper'
import { SearchAndShowAddress } from 'adhocracy4'

import { Map } from '../contrib/map/Map'
import ProjectTile from './ProjectTile'
import ProjectMarker from './ProjectMarker'
import ProjectsMapInfo from './ProjectsMapInfo'

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
          <ProjectTile project={activeProject.properties} isHorizontal isMapTile topicChoices={topicChoices} />
        </ControlWrapper>
      )}
    </>
  )
}

const ProjectsMap = ({ items, topicChoices, ...props }) => {
  return (
    <div className="projects-map">
      <ProjectsMapInfo className="projects-map-info--mobile" />
      <Map
        zoomControl={false}
        maxZoom={18}
        {...props}
        id="project-map"
        key="project-map"
        style={{ minHeight: '100%', height: '100%' }}
        className="projects-map__map"
      >
        <SearchAndShowAddress apiUrl="https://bplan-prod.liqd.net/api/addresses/" />
        <ControlWrapper position="bottomleft" className="projects-map-info__wrapper">
          <ProjectsMapInfo />
        </ControlWrapper>
        <ZoomControl position="topleft" />
        <Markers items={items} topicChoices={topicChoices} />
      </Map>
    </div>
  )
}

export default ProjectsMap
