import React from 'react'
import django from 'django'
import { classNames } from 'adhocracy4'

const translations = {
  nowText: django.gettext('now'),
  minutesAgoText: (minutes) => django.interpolate(
    django.gettext('%(minutes)sm ago'),
    { minutes },
    true
  ),
  hoursAgoText: (hours) => django.interpolate(
    django.gettext('%(hours)sh ago'),
    { hours },
    true
  ),
  yesterdayText: django.gettext('Yesterday')
}

export default function Notification ({ icon, title, body, link, linkText, isRead, timestamp }) {
  return (
    <div className={classNames('notification', !isRead && 'notification--unread')}>
      <div className="notification__icon">
        <i
          className={classNames(
            'fa-solid',
            icon === 'comment' && 'fa-comment',
            icon === 'clock' && 'fa-clock'
          )}
        />
        {!isRead && <span className="notification__unread" />}
      </div>
      <div className="notification__content">
        <div className="notification__info">
          <h3 className="notification__title">{title}</h3>
          <time className="notification__date" dateTime={new Date(timestamp).toISOString()}>
            {formatTimestamp(timestamp)}
          </time>
        </div>
        <div className={classNames('notification__panel', body && 'notification__panel--filled')}>
          {body && <p className="notification__body">{body}</p>}
          <a className="notification__link" href={link}>{linkText}</a>
        </div>
      </div>
    </div>
  )
}

function formatTimestamp (timestamp) {
  const now = new Date()
  const date = new Date(timestamp)
  const diffMs = now - date
  const diffSeconds = Math.floor(diffMs / 1000)
  const diffMinutes = Math.floor(diffSeconds / 60)
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffSeconds < 60) return translations.nowText
  if (diffMinutes < 60) return translations.minutesAgoText(diffMinutes)
  if (diffHours < 24) return translations.hoursAgoText(diffHours)
  if (diffDays === 1) return translations.yesterdayText

  return date.toLocaleDateString()
}
