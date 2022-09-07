import React from 'react'
import django from 'django'

const pageNavigationStr = django.gettext('Page navigation')
const pageNextStr = django.gettext('next page')
const pagePrevStr = django.gettext('prev page')


export const Pagination = (props) => {
  const {
    currentPage,
    nextPage,
    prevPage,
    pageCount,
  } = props

  // Creating an Array from single digit, example: 5 = [0,1,2,3,4]
  // and map to start by 1
  const pages = [...Array(pageCount).keys()].map(n => n + 1)

  const PagesLink = () => {
    let pages = []

    // display previous pages links
    let previousLinks = currentPage - 1
    for (let num = previousLinks; num <= currentPage; num++) {
        if (num < currentPage && num > 0) {
            pages.push(
              <li
                key={`page-${num}`}
                className={
                  num === currentPage
                    ? 'pagination-item active'
                    : 'pagination-item'
                  }
              >
                <button onClick={() => props.onPaginate(num)}>
                  {num}
                </button>
              </li>
            )
        }
    }

    // display next pages links
    let nextLinks = (currentPage < pageCount) ? (currentPage + 1) : currentPage
    for (let num = currentPage; num <= nextLinks; num++) {
        if (num <= pageCount) {
            pages.push(
              <li
                key={`page-${num}`}
                className={
                  num === currentPage
                    ? 'pagination-item active'
                    : 'pagination-item'
                  }
              >
                <button onClick={() => props.onPaginate(num)}>
                  {num}
                </button>
              </li>
            )
        }
    }

    return pages
}


  return (
    <nav aria-label={pageNavigationStr}>
      <ul className="pagination btn-group">
        <li className="pagination-item">
          <button
            className={!prevPage ? 'disabled' : undefined}
            onClick={() => props.onPaginate(prevPage)}
            aria-label={pagePrevStr}
          >
            <i className="fa fa-chevron-left" aria-hidden="true"/>
          </button>
        </li>

        <PagesLink />

        <li className="pagination-item">
          <button
            className={!nextPage ? 'disabled' : undefined}
            onClick={() => props.onPaginate(nextPage)}
            aria-label={pageNextStr}
          >
            <i className="fa fa-chevron-right" aria-hidden="true"/>
          </button>
        </li>
      </ul>
    </nav>
  )
}
