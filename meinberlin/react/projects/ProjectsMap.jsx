import React from 'react'
import 'leaflet.markercluster'
import { MapWithMarkers } from '../contrib/map/Map'

const ProjectsMap = ({ items, ...props }) => {
  return (
    <div className="projects-map">
      <MapWithMarkers
        scrollWheelZoom={false}
        zoomControl
        maxZoom={18}
        {...props}
        points={items.filter(item => !!item.point).map(item => ({ ...item.point, properties: item }))}
        id="project-map"
        style={{ minHeight: '100%', height: '100%' }}
        className="projects-map__map"
      />
    </div>
  )
}

export default ProjectsMap
