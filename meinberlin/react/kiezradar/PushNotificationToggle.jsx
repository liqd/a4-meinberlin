import React, { useState } from 'react'
import django from 'django'
import { ToggleSwitch } from '../contrib/ToggleSwitch'
import { updateItem } from '../contrib/helpers'

const notificationsText = django.gettext(
  'Notifications'
)
const errorUpdateNotificationText = django.gettext(
  'Failed to update push notification'
)

export default function PushNotificationToggle ({ id, apiUrl, checked: _checked, onError }) {
  const [checked, setChecked] = useState(_checked)

  const handleToggle = async (checked) => {
    onError(null)

    try {
      const response = await updateItem({ notification: checked }, apiUrl + id + '/', 'PATCH')

      if (!response.ok) {
        throw new Error(errorUpdateNotificationText)
      }
    } catch (err) {
      onError(err.message)
    }
  }

  return (
    <ToggleSwitch
      className="search-profile__toggle-switch"
      toggleSwitch={() => {
        setChecked(!checked)
        handleToggle(!checked)
      }}
      labelLeft={false}
      onSwitchStr={notificationsText}
      checked={checked}
      size="small"
    />
  )
}
