import React from 'react'
import { createRoot } from 'react-dom/client'
import NotificationsList from './NotificationsList'

function init () {
  const el = document.getElementById('notifications-react')
  const root = createRoot(el)
  const notifications = JSON.parse(el.getAttribute('data-initial-notifications'))
  const showRestricted = JSON.parse(el.getAttribute('data-show-restricted'))
  root.render(
    <React.StrictMode>
      <NotificationsList initialNotifications={notifications} showRestricted={showRestricted} />
    </React.StrictMode>)
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
