import React from 'react'
import django from 'django'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import { BrowserRouter } from 'react-router'
import { FetchItemsProvider } from '../contrib/contexts/FetchItemsProvider'
import { ListMapView } from '../contrib/map/ListMapView'

function init () {
  ReactWidget.initialise('mb', 'kiezkasse-proposals',
    function (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <BrowserRouter>
            <FetchItemsProvider {...props} isMapAndList>
              <ListMapView {...props} listStr={django.gettext('Proposals list')} mode="list" />
            </FetchItemsProvider>
          </BrowserRouter>
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
