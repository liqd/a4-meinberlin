import React from 'react'

export const Pill = (props) => {
  const {
    pillClass,
    children
  } = props

  return (
    <li className={pillClass}>
      {children}
    </li>
  )
}
