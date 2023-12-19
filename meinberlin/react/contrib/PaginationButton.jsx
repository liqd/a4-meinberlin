import React from 'react'

export const PaginationButton = (props) => {
  const disabledClass = props.isDisabled
    ? 'disabled'
    : undefined

  const itemClass = props.isActive
    ? 'active'
    : ''

  const getLabel = () => {
    if (props.type === 'num') {
      return props.pageIndex
    } else if (props.type === 'prev') {
      return (
        <>
          <i className="fa fa-chevron-left" aria-hidden="true" />
          <span className="aural">{props.prevString}</span>
        </>
      )
    } else if (props.type === 'next') {
      return <i className="fa fa-chevron-right" aria-hidden="true" />
    }
  }

  return (
    <li
      className={itemClass}
    >
      {props.isNoButton
        ? (
          <div>
            {getLabel()}
          </div>
          )
        : (
          <button
            className={disabledClass}
            onClick={() => props.onClick(props.pageIndex)}
            aria-label={props.ariaLabel}
          >
            {getLabel()}
          </button>
          )}
    </li>
  )
}
