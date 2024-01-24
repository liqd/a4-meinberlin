import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import { TopicPrioList } from './TopicPrioList.jsx'
import { BrowserRouter } from 'react-router-dom'

function init () {
  ReactWidget.initialise('mb', 'topics',
    function (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <BrowserRouter>
            <TopicPrioList {...props} />
          </BrowserRouter>
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)