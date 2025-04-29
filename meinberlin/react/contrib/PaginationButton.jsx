import React from 'react'
import { classNames } from 'adhocracy4'

export const PaginationButton = ({
  ariaLabel, total, isActive, isDisabled, isNoButton, onClick, pageIndex, prevString, type, className = ''
}) => {
  const disabledClass = isDisabled
    ? 'disabled'
    : undefined

  let itemClass = ''

  itemClass += ' ' + className

  if (type === 'prev') {
    itemClass += ' pager-item-previous'
  } else if (type === 'next') {
    itemClass += ' pager-item-next'
  } else if (type === 'current-num') {
    itemClass += ' mobile-counter'
  }

  const getLabel = () => {
    if (type === 'num') {
      return pageIndex
    } else if (type === 'current-num') {
      return pageIndex + '/' + total
    } else if (type === 'prev') {
      return (
        <>
          <i className="fa fa-chevron-left" aria-hidden="true" />
          <span className="aural">{prevString}</span>
        </>
      )
    } else if (type === 'next') {
      return <i className="fa fa-chevron-right" aria-hidden="true" />
    }
  }

  return (
    <li
      className={itemClass}
    >
      {isNoButton
        ? (
          <div>
            {getLabel()}
          </div>
          )
        : (
          <button
            className={classNames(disabledClass, isActive && 'active')}
            onClick={() => onClick(pageIndex)}
            aria-label={ariaLabel}
            disabled={isDisabled}
          >
            {getLabel()}
          </button>
          )}
    </li>
  )
}
