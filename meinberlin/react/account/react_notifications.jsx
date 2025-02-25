import React from 'react'
import { createRoot } from 'react-dom/client'
import Notifications from './Notifications'

function init () {
  const el = document.getElementById('notifications-react')
  const root = createRoot(el)
  const interactionsApiUrl = el.getAttribute('data-interactions-api-url')
  const followedProjectsApiUrl = el.getAttribute('data-followed-projects-api-url')
  const planListUrl = el.getAttribute('data-plan-list-url')
  root.render(
    <React.StrictMode>
      <Notifications
        interactionsApiUrl={interactionsApiUrl}
        followedProjectsApiUrl={followedProjectsApiUrl}
        planListUrl={planListUrl}
      />
    </React.StrictMode>)
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
