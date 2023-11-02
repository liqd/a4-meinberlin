import React from 'react'
import django from 'django'
import { toLocaleDate } from './helpers'

const translated = {
  updatedOnStr: django.gettext('updated on'),
  createdOnStr: django.gettext('created on')
}

export const CardMeta = (props) => {
  const { item } = props
  const safeLocale = props.locale ? props.locale : undefined
  const dateTime = item.modified
    ? item.modified
    : item.created
  const date = item.modified
    ? translated.updatedOnStr + ' ' + toLocaleDate(
      item.modified,
      safeLocale
    )
    : translated.createdOnStr + ' ' + toLocaleDate(
      item.created,
      safeLocale
    )

  return (
    <div className="card__meta subtitle text--meta">
      <p>
        {item.creator}
        <time dateTime={dateTime}> {date + ' - ' + item.reference_number}</time>
      </p>
    </div>
  )
}
