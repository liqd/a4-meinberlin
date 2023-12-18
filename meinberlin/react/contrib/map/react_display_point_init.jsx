import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import { MapWithMarkers } from './Map'

function init () {
  ReactWidget.initialise('mb', 'display-point', function (el) {
    const props = JSON.parse(el.getAttribute('data-attributes'))
    const root = createRoot(el)
    root.render(
      <React.StrictMode>
        <MapWithMarkers
          {...props.map}
          points={[props.map.point]}
          id="display-point"
          withoutPopup
        />
      </React.StrictMode>
    )
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
