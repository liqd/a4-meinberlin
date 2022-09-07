import React from 'react'
import django from 'django'

const pageNavigationStr = django.gettext('Page navigation')
const pageNextStr = django.gettext('next page')
const pagePrevStr = django.gettext('prev page')


export const Pagination = (props) => {
  const {
    currPageIndex,
    nextPage,
    prevPage,
    hasPrevPage,
    hasNextPage,
    pageCount,
  } = props

  // Creating an Array from single digit, example: 5 = [0,1,2,3,4]
  // and map to start by 1
  const pages = [...Array(pageCount).keys()].map(n => n + 1)

  return (
    <nav aria-label={pageNavigationStr}>
      <ul className="pagination btn-group">
        <li
          className="pagination-item"
        >
          <button
            className={!hasPrevPage ? 'disabled' : undefined}
            onClick={() => props.onPaginate(prevPage)}
            aria-label={pageNextStr}
          >
              <i className="fa fa-chevron-left" aria-hidden="true"/>
          </button>
        </li>

        {pages.map(num => (
          <li
            key={`page-${num}`}
            className={
              num === currPageIndex
                ? 'pagination-item active'
                : 'pagination-item'
              }
          >
            <button onClick={() => props.onPaginate(num)}>
              {num}
            </button>
          </li>
        ))}

        <li
          className={`pagination-item ${!hasNextPage && 'disabled'}`}
        >
          <button
            className={!hasNextPage ? 'disabled' : undefined}
            onClick={() => props.onPaginate(nextPage)}
            aria-label={pagePrevStr}
          >
              <i className="fa fa-chevron-right" aria-hidden="true"/>
          </button>
        </li>
      </ul>
    </nav>
  )
}
