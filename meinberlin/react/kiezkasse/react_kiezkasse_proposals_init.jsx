import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import { KiezkasseProposalsList } from './KiezkasseProposalsList.jsx'
import { BrowserRouter } from 'react-router-dom'

function init () {
  ReactWidget.initialise('mb', 'kiezkasse-proposals',
    function (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <BrowserRouter>
            <KiezkasseProposalsList {...props} />
          </BrowserRouter>
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
