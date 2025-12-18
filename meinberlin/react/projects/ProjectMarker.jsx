/* eslint-disable no-restricted-syntax */
import React, { useRef } from 'react'
import GeoJsonMarker, {
  makeIcon
} from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/GeoJsonMarker'
import { Popup } from 'react-leaflet'
import ProjectTile from './ProjectTile'

const ProjectMarker = ({ project, onOpen, onClose, topicChoices }) => {
  const ref = useRef(null)
  const tileRef = useRef(null)
  const markerElementRef = useRef(null)

  // Generate a unique ID for this popup
  const popupId = `popup-${project.properties.id || project.properties.slug || Date.now()}`

  const focusFirstInteractiveElement = () => {
    setTimeout(() => { if (tileRef.current) { tileRef.current.focus() } }, 100)
  }

  const setMarkerElementRef = () => {
    const markerElement = ref.current?.getElement?.()
    if (markerElement) {
      markerElement.tabIndex = -1
      markerElementRef.current = markerElement
    }
  }

  const focusMarkerElement = () => {
    const element = markerElementRef.current ?? ref.current?.getElement?.()
    if (element) {
      element.focus()
    }
  }

  const announcePopup = (message) => {
    const liveRegion = document.getElementById('map-live-region')
    if (liveRegion) {
      liveRegion.textContent = message
    }
  }

  return (
    <GeoJsonMarker
      ref={ref}
      key={project.properties.title}
      feature={project}
      eventHandlers={{
        popupopen: (e) => {
          ref.current?.setIcon(makeIcon('/static/images/map_pin_active.svg'))
          setMarkerElementRef()
          onOpen(e)
          focusFirstInteractiveElement()
          announcePopup(`Popup opened: ${project.properties.title}`)
        },
        popupclose: (e) => {
          ref.current?.setIcon(makeIcon())
          focusMarkerElement()
          onClose(e)
          announcePopup('Popup closed')
        }
      }}
    >
      <Popup
        className="projects-map__popup"
        offset={[0, 225]}
        maxWidth={400}
        minWidth={400}
        // Remove role and aria-modal from here - add them to wrapper div below
      >
        {/* Wrapper div with proper ARIA attributes for the dialog */}
        <div
          role="dialog"
          aria-modal="false"
          aria-label={`Details: ${project.properties.title}`}
          id={popupId}
        >
          <ProjectTile
            project={project.properties}
            isHorizontal
            topicChoices={topicChoices}
            isMapTile
            ref={tileRef}
          />
        </div>
      </Popup>
    </GeoJsonMarker>
  )
}

export default ProjectMarker
