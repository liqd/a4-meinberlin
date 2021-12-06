import React from 'react'

export const CountComponent = (props) => {
  const {
    activeClass,
    inactiveClass,
    countText,
    counter
  } = props

  return (
    <div
      className={counter > 0 ? activeClass : inactiveClass}
    >
      <span>{countText}</span>
    </div>
  )
}
