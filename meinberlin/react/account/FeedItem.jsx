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

export default function FeedItem ({ icon, title, body, meta = [], link, linkText, isRead, timestamp }) {
  return (
    <article className={classNames('feed-item', !isRead && 'feed-item--unread')}>
      <div className="feed-item__icon">
        <i
          className={classNames(
            'fa-solid',
            icon === 'comment' && 'fa-comment',
            icon === 'clock' && 'fa-clock'
          )}
        />
        {!isRead && <span className="feed-item__unread" />}
      </div>
      <div className="feed-item__content">
        <div className="feed-item__info">
          <div>
            <h3 className={classNames('feed-item__title', isRead && 'feed-item__title--read')}>{title}</h3>
            {meta.length > 0 && (
              <ul className="feed-item__meta">
                {meta.map((item, index) => (
                  <li key={item + index} className="feed-item__meta-item">{item}</li>
                ))}
              </ul>
            )}
          </div>
          <time
            className="feed-item__date"
            title={new Date(timestamp).toLocaleString()}
            dateTime={new Date(timestamp).toISOString()}
          >
            {formatTimestamp(timestamp)}
          </time>
        </div>
        <div className={classNames('feed-item__panel', body && 'feed-item__panel--filled')}>
          {body && <p className="feed-item__body">{body}</p>}
          <a className="feed-item__link" href={link}>{linkText}</a>
        </div>
      </div>
    </article>
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
