import { DetailVoteButton } from './DetailVoteButton.jsx'
import React from 'react'
import ReactDOM from 'react-dom'

export function renderVoteButton (el) {
  const props = el.getAttribute('data-attributes')
  ReactDOM.render(<DetailVoteButton {...props} />, el)
}
