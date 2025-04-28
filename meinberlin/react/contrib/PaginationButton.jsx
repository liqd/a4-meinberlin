import React from 'react'

export const PaginationButton = ({
  ariaLabel, isActive, isDisabled, isNoButton, onClick, pageIndex, prevString, type
}) => {
  const disabledClass = isDisabled
    ? 'disabled'
    : undefined

  const itemClass = isActive
    ? 'active'
    : ''

  const getLabel = () => {
    if (type === 'num') {
      return pageIndex
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
            className={disabledClass}
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
