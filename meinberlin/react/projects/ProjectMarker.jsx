import React, { useRef } from 'react'
import GeoJsonMarker, {
  makeIcon
} from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/GeoJsonMarker'
import { Popup } from 'react-leaflet'
import ProjectTile from './ProjectTile'

const ProjectMarker = ({ project, onOpen, onClose, topicChoices }) => {
  const ref = useRef(null)

  return (
    <GeoJsonMarker
      ref={ref}
      key={project.properties.title}
      feature={project}
      eventHandlers={{
        popupopen: (e) => {
          ref.current?.setIcon(makeIcon('/static/images/map_pin_active.svg'))
          onOpen(e)
        },
        popupclose: (e) => {
          ref.current?.setIcon(makeIcon())
          onClose(e)
        }
      }}
    >
      <Popup
        className="projects-map__popup"
        offset={[0, 295]}
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
  )
}

export default ProjectMarker
