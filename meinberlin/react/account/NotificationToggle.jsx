import django from 'django'
import React from 'react'
import { ToggleSwitch } from '../contrib/ToggleSwitch'

const emailStr = django.gettext('Email')
const inAppNotificationStr = django.gettext('In-app')

const NotificationToggle = ({ notification, notificationState, name, onToggle }) => {
  const activityFeedName = notification.activityFeedName
  const emailToggleId = name + '-email'
  const inAppToggleId = name + '-inapp'
  return (
    <fieldset>
      <legend>
        <h3>{notification.title}</h3>
      </legend>
      <p>{notification.description}</p>
      <div className="flexbox">
        <ToggleSwitch
          uniqueId={emailToggleId}
          onSwitchStr={emailStr}
          labelLeft={false}
          checked={notificationState[name]}
          toggleSwitch={() => onToggle(name)}
          size="small"
        />
        {activityFeedName &&
          <ToggleSwitch
            className="ml-1"
            uniqueId={inAppToggleId}
            onSwitchStr={inAppNotificationStr}
            labelLeft={false}
            checked={notificationState[activityFeedName]}
            toggleSwitch={() => onToggle(activityFeedName)}
            size="small"
          />}
      </div>
    </fieldset>
  )
}

export default NotificationToggle
