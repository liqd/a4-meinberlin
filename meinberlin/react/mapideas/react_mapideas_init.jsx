import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { widget as ReactWidget } from 'adhocracy4'
import { MapIdeaList } from './MapIdeaList'

function init () {
  ReactWidget.initialise('mb', 'map_ideas',
    function (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <BrowserRouter>
            <MapIdeaList {...props} />
          </BrowserRouter>
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
