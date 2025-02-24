import React, { useEffect, useState } from 'react'
import django from 'django'
import Spinner from '../contrib/Spinner'
import { alert as Alert, classNames } from 'adhocracy4'

const translations = {
  notificationsText: django.gettext('Notifications'),
  notificationsDescriptionText: django.gettext('Here you can see all the interactions you have with other users on meinBerlin.'),
  errorText: django.gettext('Error'),
  errorNotificationsText: django.gettext('Failed to fetch notifications'),
  moderatorReplieIdeaText: (title) => django.interpolate(
    django.gettext('A moderator has responded to your idea in %(title)s'),
    { title },
    true
  ),
  userRepliedIdeaText: (name, title) => django.interpolate(
    django.gettext('%(name)s has replied to your idea in %(title)s'),
    { name, title },
    true
  ),
  moderatorRepliedCommentText: (title) => django.interpolate(
    django.gettext('A moderator has responded to your comment in %(title)s'),
    { title },
    true
  ),
  userRepliedCommentText: (name, title) => django.interpolate(
    django.gettext('%(name)s has replied to your comment in %(title)s'),
    { name, title },
    true
  ),
  userRatedIdeaText: (title) => django.interpolate(
    django.gettext('A user has rated your idea in %(title)s'),
    { title },
    true
  ),
  userRatedCommentText: (title) => django.interpolate(
    django.gettext('A user has rated your comment in %(title)s'),
    { title },
    true
  ),
  viewIdeaText: django.gettext('View idea'),
  viewCommentText: django.gettext('View comment'),
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

export default function Notifications ({ notificationsApiUrl }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [notifications, setNotifications] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(notificationsApiUrl)

        if (!response.ok) {
          throw new Error(translations.errorNotificationsText)
        }

        const data = await response.json()
        setNotifications(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="notifications" aria-live="polite">
      {loading
        ? <Spinner />
        : error
          ? <Alert type="danger" message={translations.errorText + ': ' + error} />
          : (
            <>
              <h2 className="notifications__title">
                {translations.notificationsText} {notifications && <span className="notifications__count">{notifications.count}</span>}
              </h2>
              <p className="notifications__description">{translations.notificationsDescriptionText}</p>
              {notifications &&
                [...notifications.results].reverse().map(({ read, action }) => {
                  const { type, timestamp, link, ...rest } = action
                  const text = getNotifcationText({ type, ...rest })

                  if (!text) {
                    return null
                  }

                  const { title, body, linkText } = text

                  return (
                    <Notification
                      key={timestamp}
                      icon={type === 'comment' ? 'comment' : 'clock'}
                      title={title}
                      body={body}
                      link={link}
                      linkText={linkText}
                      isRead={read}
                      timestamp={timestamp}
                    />
                  )
                })}
            </>
            )}
    </div>
  )
}

function Notification ({ icon, title, body, link, linkText, isRead, timestamp }) {
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

function getNotifcationText (action) {
  const { type, source, body, actor, project } = action

  switch (type) {
    case 'comment':
      switch (source) {
        case 'idea':
        case 'mapidea':
          if (actor.is_moderator) {
            return {
              title: translations.moderatorReplieIdeaText(project.title),
              body,
              linkText: translations.viewCommentText
            }
          }

          return {
            title: translations.userRepliedIdeaText(actor.username, project.title),
            body,
            linkText: translations.viewCommentText
          }

        case 'comment':
          if (actor.is_moderator) {
            return {
              title: translations.moderatorRepliedCommentText(project.title),
              body,
              linkText: translations.viewCommentText
            }
          }

          return {
            title: translations.userRepliedCommentText(actor.username, project.title),
            body,
            linkText: translations.viewCommentText
          }
      }
      break

    case 'rating':
      switch (source) {
        case 'idea':
        case 'mapidea':
          return {
            title: translations.userRatedIdeaText(project.title),
            linkText: translations.viewIdeaText
          }

        case 'comment':
          return {
            title: translations.userRatedCommentText(project.title),
            body,
            linkText: translations.viewCommentText
          }
      }
  }
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
