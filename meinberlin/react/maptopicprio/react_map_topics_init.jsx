import React from 'react'
import django from 'django'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import { BrowserRouter } from 'react-router'
import { ListMapView } from '../contrib/map/ListMapView'
import { FetchItemsProvider } from '../contrib/contexts/FetchItemsProvider'

function init () {
  ReactWidget.initialise('mb', 'map-topics',
    function (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <BrowserRouter>
            <FetchItemsProvider {...props} isMapAndList>
              <ListMapView {...props} listStr={django.gettext('Map topics list')} />
            </FetchItemsProvider>
          </BrowserRouter>
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
