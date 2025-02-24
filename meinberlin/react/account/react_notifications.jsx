import React from 'react'
import { createRoot } from 'react-dom/client'
import Notifications from './Notifications'

function init () {
  const el = document.getElementById('notifications-react')
  const root = createRoot(el)
  const notificationsApiUrl = el.getAttribute('data-notifications-api-url')
  console.log(notificationsApiUrl)
  root.render(
    <React.StrictMode>
      <Notifications
        notificationsApiUrl={notificationsApiUrl}
      />
    </React.StrictMode>)
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
