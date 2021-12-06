import * as ReactVote from './react_vote_button.jsx'
import { widget as ReactWidget } from 'adhocracy4'

function init () {
  ReactWidget.initialise('mb', 'proposal_votes', ReactVote.renderVoteButton)
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
