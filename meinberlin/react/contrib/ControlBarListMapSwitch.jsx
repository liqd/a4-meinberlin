import React from 'react'
import django from 'django'
import { useSearchParams } from 'react-router-dom'

export const ControlBarListMapSwitch = () => {
  // FIXME: to be changed, once Map is in React

  const [queryParams, setQueryParams] = useSearchParams()

  const handleClick = () => {
    queryParams.set('mode', 'map')
    setQueryParams(queryParams)
    location.reload()
  }

  return (
    <div className="control-bar__list-map-switch">
      <div
        className="button button--light button--fulltone"
        aria-label={django.gettext('View as list')}
      >
        <span className="fa fa-list" aria-hidden="true" />&nbsp;
        {django.gettext('List')}
      </div>
      <button
        className="button button--light"
        onClick={handleClick}
        aria-label={django.gettext('View as map')}
      >
        <span className="fa fa-map" aria-hidden="true" />&nbsp;
        {django.gettext('Map')}
      </button>
    </div>
  )
}
