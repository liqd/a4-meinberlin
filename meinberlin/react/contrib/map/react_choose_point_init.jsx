import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import { Map } from './Map'
import ChoosePointMap
  from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/ChoosePointMap'

function init () {
  ReactWidget.initialise('a4', 'react-choose-point', function (el) {
    const props = JSON.parse(el.getAttribute('data-attributes'))
    const root = createRoot(el)
    root.render(
      <React.StrictMode>
        <ChoosePointMap
          BaseMap={Map}
          input={el.nextElementSibling}
          apiUrl="/api/geodaten/search"
          {...props.map}
        />
      </React.StrictMode>
    )
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
