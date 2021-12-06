import * as ReactBudget from './react_proposals.jsx'
import { widget as ReactWidget } from 'adhocracy4'

function init () {
  ReactWidget.initialise('mb', 'proposals', ReactBudget.renderProposals)
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
