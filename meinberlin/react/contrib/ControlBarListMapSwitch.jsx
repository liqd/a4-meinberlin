import React from 'react'
import django from 'django'
import { useSearchParams } from 'react-router-dom'

const translated = {
  viewMode: django.gettext('View mode'),
  viewList: django.gettext('View as list'),
  list: django.gettext('List'),
  viewMap: django.gettext('View as map'),
  map: django.gettext('Map')
}

export const ControlBarListMapSwitch = () => {
  // FIXME: to be changed, once Map is in React and made more a11y compliant

  const [queryParams, setQueryParams] = useSearchParams()

  const handleClick = () => {
    queryParams.set('mode', 'map')
    setQueryParams(queryParams)
    location.reload()
  }

  return (
    <div className="control-bar__list-map-switch-container">
      <span className="text--strong">{translated.viewMode}</span>
      <div className="control-bar__list-map-switch">
        <div
          className="button button--light button--fulltone"
          aria-label={translated.viewList}
        >
          <span className="fa fa-list" aria-hidden="true" />&nbsp;
          {translated.list}
        </div>
        <button
          className="button button--light"
          onClick={handleClick}
          aria-label={translated.viewMap}
        >
          <span className="fa fa-map" aria-hidden="true" />&nbsp;
          {translated.map}
        </button>
      </div>
    </div>
  )
}
