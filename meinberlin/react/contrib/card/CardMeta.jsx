import React from 'react'
import { toLocaleDate } from '../helpers'

export const CardMeta = (props) => {
  const { item } = props
  const safeLocale = props.locale ? props.locale : undefined
  const dateTime = item.modified
    ? item.modified
    : item.created
  const date = toLocaleDate(dateTime, safeLocale)

  return (
    <div className="card__meta subtitle text--meta">
      <p>
        {item.creator} <time dateTime={dateTime}>{date}</time>
      </p>
    </div>
  )
}
