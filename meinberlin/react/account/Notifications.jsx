import React, { useEffect, useState } from 'react'
import django from 'django'
import Spinner from '../contrib/Spinner'
import { alert as Alert } from 'adhocracy4'

const errorText = django.gettext('Error')
const errorNotificationsText = django.gettext(
  'Failed to fetch notifications'
)

export default function Notifications () {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [notifications, setNotifications] = useState(null)

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch('/api/notifications/')

        if (!response.ok) {
          throw new Error(errorNotificationsText)
        }

        const data = await response.json()
        setNotifications(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchNotifications()
  }, [])

  return (
    <div aria-live="polite">
      {loading
        ? <Spinner />
        : error
          ? (
            <div className="kiezradar__error">
              <Alert type="danger" message={errorText + ': ' + errorNotificationsText} />
            </div>
            )
          : (
            <>
              {JSON.stringify(notifications)}
            </>
            )}
    </div>
  )
}
