import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import SearchProfiles from './SearchProfiles'

function init () {
  ReactWidget.initialise('mb', 'kiezradar-search-profiles', function (el) {
    const props = JSON.parse(el.getAttribute('data-attributes'))
    const root = createRoot(el)
    root.render(
      <React.StrictMode>
        <SearchProfiles {...props} />
      </React.StrictMode>
    )
  })
}

document.addEventListener('DOMContentLoaded', init, false)
