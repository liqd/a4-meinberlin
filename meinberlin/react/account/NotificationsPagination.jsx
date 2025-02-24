import React from 'react'
import { classNames } from 'adhocracy4'

export default function NotificationsPagination ({ page, totalPages, setPage }) {
  if (!totalPages || totalPages < 2) return null

  const pageNumbers = getPageNumbers(totalPages, page)

  return (
    <div className="notifications__pagination">
      <button
        className="notifications__pagination-item notifications__pagination-button"
        disabled={page <= 1}
        onClick={() => setPage(page - 1)}
      >
        <i className="fa-solid fa-angle-left notifications__pagination-icon" />
      </button>

      {pageNumbers.map((num, index) =>
        num === '...'
          ? <span key={index} className="notifications__pagination-item">...</span>
          : (
            <button
              key={num}
              className={classNames('notifications__pagination-item notifications__pagination-button', page === num && 'notifications__pagination-item--active')}
              onClick={() => setPage(num)}
            >
              <span>{num}</span>
            </button>
            )
      )}

      <button
        className="notifications__pagination-item notifications__pagination-button"
        disabled={page >= totalPages}
        onClick={() => setPage(page + 1)}
      >
        <i className="fa-solid fa-angle-right notifications__pagination-icon" />
      </button>
    </div>
  )
}

function getPageNumbers (totalPages, page) {
  const pages = []
  const maxVisiblePages = 5

  if (totalPages <= maxVisiblePages + 2) {
    for (let i = 1; i <= totalPages; i++) pages.push(i)
  } else {
    pages.push(1)

    if (page > 3) pages.push('...')

    const start = Math.max(2, page - 1)
    const end = Math.min(totalPages - 1, page + 1)

    for (let i = start; i <= end; i++) pages.push(i)

    if (page < totalPages - 2) pages.push('...')

    pages.push(totalPages)
  }

  return pages
}
