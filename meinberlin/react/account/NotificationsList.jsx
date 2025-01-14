import React, { useState } from 'react'
import django from 'django'
import { ToggleSwitch } from '../contrib/ToggleSwitch'
import NotificationToggle from './NotificationToggle'

const notifications = [
  {
    header: django.gettext('Project-Related Notifications'),
    notifications: {
      email_newsletter: {
        title: django.gettext('E-Mail Newsletter'),
        description: django.gettext('Receive newsletters with updates and news about the projects you follow via e-mail.')
      },
      participation_start: {
        title: django.gettext('Participation Start'),
        description: django.gettext('Receive a notification when a participation begins in a project you follow.'),
        showInActivityFeed: true
      },
      participation_end: {
        title: django.gettext('Participation End'),
        description: django.gettext('Receive a notification when a participation is near its end in a project you follow.'),
        showInActivityFeed: true
      },
      new_events: {
        title: django.gettext('Event'),
        description: django.gettext('Receive notifications for upcoming events in projects you follow.'),
        showInActivityFeed: true
      }
    }
  },
  {
    header: django.gettext('Interactions with Other Users or Moderation'),
    notifications: {
      reactions: {
        title: django.gettext('Reactions of other users'),
        description: django.gettext('Receive a notification when someone reacts to your contribution with a comment.')
      },
      moderation_reactions: {
        title: django.gettext('Reactions of moderation'),
        description: django.gettext('Receive a notification for feedback and status changes of your idea from the moderation.')
      }
    }
  },
  {
    header: django.gettext('Notifications for Initiators and Moderators'),
    restricted: true,
    notifications: {
      new_project_in_organisation: {
        title: django.gettext('New Project in Your Organization'),
        description: django.gettext('Receive a notification when a new project is created in your organization.')
      },
      new_contribution_in_moderated_project: {
        title: django.gettext('New Contribution in a Moderated Project'),
        description: django.gettext('Receive a notification when a new contribution is added to a project you moderate.')
      }
    }
  }
]

const NotificationsList = ({
  initialNotifications,
  showRestricted = false
}) => {
  const [notificationsState, setNotificationsState] = useState(notifications.reduce((acc, notification) => {
    if (notification.restricted && !showRestricted) return acc

    Object.keys(notification.notifications).forEach(key => {
      acc[key] = {
        email: initialNotifications[key]?.email,
        activityFeed: initialNotifications[key]?.activity_feed
      }
    })

    return acc
  }, {}))
  const masterToggles = notifications
    .filter((n) => !n.restricted || (n.restricted && showRestricted))
    .map((n, i) => Object.keys(n.notifications).some((key) => notificationsState[key].email))

  const onToggle = (type, key, force = null) => {
    const newState = { ...notificationsState }
    if (force !== null) newState[key][type] = force
    else newState[key][type] = !notificationsState[key][type]
    setNotificationsState(newState)
  }

  return (
    <ul className="list--clean">
      {notifications.map((notification, index) => {
        if (notification.restricted && !showRestricted) return null

        return (
          <li key={notification.header}>
            <div className="actionable-list__header">
              <h2>{notification.header}</h2>
              <ToggleSwitch
                className="actionable-list__header__action"
                uniqueId={'masterToggle' + index}
                checked={masterToggles[index]}
                toggleSwitch={() => {
                  Object.keys(notification.notifications).forEach(key => {
                    onToggle('email', key, !masterToggles[index])
                  })
                }}
              />
            </div>
            <ul className="actionable-list">
              {Object.entries(notification.notifications).map(([key, value]) => (
                <li key={key} className="actionable-list__item actionable-list__item--hide-last-line">
                  <NotificationToggle
                    id={key}
                    notification={value}
                    notificationState={notificationsState[key]}
                    onToggle={(type) => onToggle(type, key)}
                  />
                </li>
              ))}
            </ul>
          </li>
        )
      })}
    </ul>
  )
}

export default NotificationsList
