import React from 'react'
import L from 'leaflet'
import ReactDOM from 'react-dom'
import {
  createContainerComponent,
  createControlHook,
  createElementHook,
  createElementObject,
  extendContext
} from '@react-leaflet/core'
import ProjectTile from './ProjectTile'

// Create the custom control class
const ProjectMapOverlayControl = L.Control.extend({
  options: {
    position: 'bottomleft'
  },

  onAdd: function (map) {
    this._map = map
    this._container = L.DomUtil.create('div', 'project-overlay-control')

    if (this._content) {
      this._container.appendChild(this._content)
    }

    L.DomEvent.disableClickPropagation(this._container)
    L.DomEvent.disableScrollPropagation(this._container)

    return this._container
  },

  onRemove: function (map) {
    if (this._container) {
      ReactDOM.unmountComponentAtNode(this._container)
      L.DomUtil.remove(this._container)
      this._container = null
    }
  },

  addTo: function (map) {
    L.Control.prototype.addTo.call(this, map)
    this._container.classList.remove('leaflet-control')
    return this
  }
})

const useProjectMapOverlayElement = createElementHook((props, context) => {
  const { position, children } = props

  const control = new ProjectMapOverlayControl({ position })

  // Create a div for React content
  const contentDiv = L.DomUtil.create('div')
  ReactDOM.render(children, contentDiv)
  control._content = contentDiv

  return createElementObject(control, extendContext(context, {
    overlayContainer: control
  }))
})

const useProjectMapOverlay = createControlHook(useProjectMapOverlayElement)
const ProjectMapOverlayContainer = createContainerComponent(useProjectMapOverlay)

const ProjectMapOverlay = ({ project, topicChoices, position = 'bottomleft', ...props }) => {
  return project
    ? (
      <ProjectMapOverlayContainer position={position} {...props}>
        <ProjectTile project={project} isHorizontal isMapTile topicChoices={topicChoices} />
      </ProjectMapOverlayContainer>
      )
    : null
}

export default ProjectMapOverlay
