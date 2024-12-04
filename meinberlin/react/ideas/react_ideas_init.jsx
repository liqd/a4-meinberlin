import React from 'react'
import django from 'django'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import { widget as ReactWidget } from 'adhocracy4'
import { FetchItemsProvider } from '../contrib/contexts/FetchItemsProvider'
import { CardList } from '../contrib/card/CardList'

function init () {
  ReactWidget.initialise('mb', 'ideas',
    function (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <BrowserRouter>
            <FetchItemsProvider {...props}>
              <CardList
                apiUrl={props.ideas_api_url}
                listStr={django.gettext('Ideas list')}
                cardStatus
                cardMeta
              />
            </FetchItemsProvider>
          </BrowserRouter>
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
