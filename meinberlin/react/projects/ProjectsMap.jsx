import React from 'react'
import 'leaflet.markercluster'
import { MapWithMarkers } from '../contrib/map/Map'

const ProjectsMap = ({ items, ...props }) => {
  return (
    <MapWithMarkers
      scrollWheelZoom={false}
      zoomControl
      maxZoom={18}
      {...props}
      points={items.filter(item => !!item.point).map(item => ({ ...item.point, properties: item }))}
      id="project-map"
      style={{}}
      className="projects-map"
    />
  )
}

export default ProjectsMap
