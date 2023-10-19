import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import { IdeaList } from './IdeaList.jsx'

function init () {
  ReactWidget.initialise('mb', 'ideas',
    function (el) {
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <IdeaList />
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
