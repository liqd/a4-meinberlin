import React from 'react'
import django from 'django'

const loading = django.gettext('loading')

export default function Loading () {
  return (
    <div className="kiezradar__loading" aria-label={loading}>
      {loading}...
    </div>
  )
}
