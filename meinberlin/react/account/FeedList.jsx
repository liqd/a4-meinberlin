import React, { useEffect, useState } from 'react'
import django from 'django'
import Spinner from '../contrib/Spinner'
import { alert as Alert, classNames } from 'adhocracy4'
import { updateItem } from '../contrib/helpers'

const translations = {
  errorText: django.gettext('Error'),
  errorNotificationsText: django.gettext('Failed to fetch notifications'),
  markAllAsRead: django.gettext('Mark All As Read')
}

const PAGE_SIZE = 3

export default function FeedList ({ title, description, descriptionNoItems, buttonText, apiUrl, link, renderFeedItem }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [notifications, setNotifications] = useState([])
  const [page, setPage] = useState(1)

  const totalPages = Math.ceil(notifications.length / PAGE_SIZE)
  const paginatedNotifications = notifications.slice(
    (page - 1) * PAGE_SIZE,
    page * PAGE_SIZE
  )
  const unreadCount = notifications.filter(
    (notification) => !notification.read
  ).length

  useEffect(() => {
    const fetchAllNotifications = async () => {
      try {
        setLoading(true)
        setError(null)

        let allNotifications = []
        let currentPage = 1
        let totalCount = 0

        do {
          const response = await fetch(
            apiUrl + '?page=' + currentPage + '&page_size=50'
          )

          if (!response.ok) {
            throw new Error(translations.errorNotificationsText)
          }

          const data = await response.json()

          if (currentPage === 1) {
            totalCount = data.count
          }

          allNotifications = [...allNotifications, ...data.results]
          currentPage++
        } while (allNotifications.length < totalCount)

        setNotifications(allNotifications)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchAllNotifications()
  }, [])

  const handleMarkAllAsRead = async () => {
    try {
      setError(null)

      const response = await updateItem({ read: true }, apiUrl + '?page_size=' + notifications.length, 'POST')

      if (!response.ok) {
        throw new Error(translations.errorNotificationsText)
      }

      const data = await response.json()
      setNotifications(data.results)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="feed-list" aria-live="polite">
      {loading
        ? <Spinner />
        : error
          ? <Alert type="danger" message={translations.errorText + ': ' + error} />
          : (
            <>
              <div className="feed-list__text">
                <div>
                  <h2 className="feed-list__title">
                    {title}{' '}
                    {unreadCount > 0 && (
                      <span className="feed-list__count">{unreadCount}</span>
                    )}
                  </h2>
                  <p className="feed-list__description">
                    {notifications.length > 0 ? description : descriptionNoItems}
                  </p>
                  {notifications.length === 0 && <a className="button" href={link}>{buttonText}</a>}
                </div>
                {unreadCount > 0 && (
                  <div className="feed-list__mark-as-read">
                    <button className="feed-list__mark-as-read-button" onClick={handleMarkAllAsRead}>
                      <i className="fa-solid fa-list-check mr-1" />
                      {translations.markAllAsRead}
                    </button>
                  </div>
                )}
              </div>
              {paginatedNotifications.map((notification, index) =>
                renderFeedItem(notification, index)
              )}
              {totalPages > 1 && (
                <Pagination
                  page={page}
                  setPage={setPage}
                  totalPages={totalPages}
                />
              )}
            </>)}
    </div>
  )
}

function Pagination ({ page, setPage, totalPages }) {
  const maxVisiblePages = 5
  const startPage = Math.max(1, page - Math.floor(maxVisiblePages / 2))
  const endPage = Math.min(totalPages, startPage + maxVisiblePages - 1)
  const pageNumbers = Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i)

  return (
    <div className="feed-list__pagination">
      <button
        className="feed-list__pagination-item feed-list__pagination-button"
        disabled={page === 1}
        onClick={() => setPage(page - 1)}
      >
        <i className="fa-solid fa-angle-left feed-list__pagination-icon" />
      </button>

      {startPage > 1 && (
        <span key="start-ellipsis" className="feed-list__pagination-item">
          ...
        </span>
      )}

      {pageNumbers.map((pageNum) => (
        <button
          key={pageNum}
          className={classNames(
            'feed-list__pagination-item feed-list__pagination-button',
            page === pageNum && 'feed-list__pagination-item--active'
          )}
          onClick={() => setPage(pageNum)}
        >
          {pageNum}
        </button>
      ))}

      {endPage < totalPages && (
        <span key="end-ellipsis" className="feed-list__pagination-item">
          ...
        </span>
      )}

      <button
        className="feed-list__pagination-item feed-list__pagination-button"
        disabled={page === totalPages}
        onClick={() => setPage(page + 1)}
      >
        <i className="fa-solid fa-angle-right feed-list__pagination-icon" />
      </button>
    </div>
  )
}
