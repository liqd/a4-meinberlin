import React, { useEffect, useState } from 'react'
import django from 'django'
import Spinner from '../contrib/Spinner'
import { alert as Alert } from 'adhocracy4'
import Notification from './Notification'
import NotificationsPagination from './NotificationsPagination'

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
  viewCommentText: django.gettext('View comment')
}

export default function Notifications ({ notificationsApiUrl }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [notifications, setNotifications] = useState(null)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(notificationsApiUrl + '?page=' + page)

        if (!response.ok) {
          throw new Error(translations.errorNotificationsText)
        }

        const data = await response.json()
        setNotifications(data)
        setTotalPages(Math.ceil(data.count / 10))
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [page])

  return (
    <div className="notifications" aria-live="polite">
      {loading
        ? <Spinner />
        : error
          ? <Alert type="danger" message={translations.errorText + ': ' + error} />
          : (
            <>
              <h2 className="notifications__title">
                {translations.notificationsText}
              </h2>
              <p className="notifications__description">{translations.notificationsDescriptionText}</p>
              {notifications &&
                notifications.results.map(({ read, action }) => {
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
      {totalPages && <NotificationsPagination page={page} totalPages={totalPages} setPage={setPage} />}
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
