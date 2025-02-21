import React from 'react'
import { createRoot } from 'react-dom/client'
import Notifications from './Notifications'

function init () {
  const el = document.getElementById('notifications-react')
  const root = createRoot(el)
  root.render(
    <React.StrictMode>
      <Notifications />
    </React.StrictMode>)
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
