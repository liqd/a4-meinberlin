import React from 'react'
import django from 'django'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { widget as ReactWidget } from 'adhocracy4'
import { FetchItemsProvider } from '../contrib/contexts/FetchItemsProvider'
import { ListMapView } from '../contrib/map/ListMapView'

function init () {
  ReactWidget.initialise('mb', 'map-ideas',
    function (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <BrowserRouter>
            <FetchItemsProvider {...props} isMapAndList>
              <ListMapView {...props} listStr={django.gettext('Map Ideas list')} />
            </FetchItemsProvider>
          </BrowserRouter>
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
