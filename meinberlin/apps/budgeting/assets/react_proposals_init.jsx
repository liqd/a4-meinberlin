import React from 'react'
import ReactDOM from 'react-dom'
import { widget as ReactWidget } from 'adhocracy4'
import { BudgetingProposalList } from './BudgetingProposalList.jsx'
import { ApiProvider } from '../../contrib/assets/ApiProvider'

function init () {
  ReactWidget.initialise('mb', 'proposals', function (el) {
    const props = JSON.parse(el.getAttribute('data-attributes'))
    ReactDOM.render(
      <ApiProvider>
        <BudgetingProposalList {...props} />
      </ApiProvider>,
      el
    )
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
