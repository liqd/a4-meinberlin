import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import { Map } from './Map'
import AddMarkerControl
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/AddMarkerControl'

function init () {
  ReactWidget.initialise('mb', 'choose-point', function (el) {
    const props = JSON.parse(el.getAttribute('data-attributes'))
    const root = createRoot(el)
    root.render(
      <React.StrictMode>
        <Map {...props.map} id="choose-point">
          <AddMarkerControl input={el.nextElementSibling} point={props.map.point} />
        </Map>
      </React.StrictMode>
    )
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
