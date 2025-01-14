import django from 'django'
import React from 'react'
import { ToggleSwitch } from '../contrib/ToggleSwitch'

const emailStr = django.gettext('E-Mail')
const activityFeedStr = django.gettext('Activity Feed')

const NotificationToggle = ({ notification, notificationState, id, onToggle }) => {
  return (
    <>
      <h3>{notification.title}</h3>
      <p>{notification.description}</p>
      <div className="flexbox">
        <ToggleSwitch
          uniqueId={id}
          onSwitchStr={emailStr}
          labelLeft={false}
          checked={notificationState.email}
          toggleSwitch={() => onToggle('email')}
        />
        {notification.showInActivityFeed &&
          <ToggleSwitch
            className="ml-1"
            uniqueId={id}
            onSwitchStr={activityFeedStr}
            labelLeft={false}
            checked={notificationState.activityFeed}
            toggleSwitch={() => onToggle('activityFeed')}
          />}
      </div>
    </>
  )
}

export default NotificationToggle
