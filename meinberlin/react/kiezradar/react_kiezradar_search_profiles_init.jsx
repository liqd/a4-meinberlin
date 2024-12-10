import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import Dummy from './dummy'

function init () {
  ReactWidget.initialise('mb', 'kiezradar-search-profiles',
    function (el) {
      // const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <Dummy />
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
