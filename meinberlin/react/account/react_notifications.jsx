import React from 'react'
import { createRoot } from 'react-dom/client'
import Notifications from './Notifications'

function init () {
  const el = document.getElementById('notifications-react')
  const root = createRoot(el)
  const interactionsApiUrl = el.getAttribute('data-interactions-api-url')
  root.render(
    <React.StrictMode>
      <Notifications
        interactionsApiUrl={interactionsApiUrl}
      />
    </React.StrictMode>)
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
