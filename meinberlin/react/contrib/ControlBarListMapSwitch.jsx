import React from 'react'
import django from 'django'
import { useSearchParams } from 'react-router-dom'

const ViewModeButton = ({ active, handleClick, children, ...rest }) => {
  if (active) {
    return (
      <div
        className="button button--light button--fulltone"
        {...rest}
      >
        {children}
      </div>
    )
  } else {
    return (
      <button
        className="button button--light"
        onClick={handleClick}
        {...rest}
      >
        {children}
      </button>
    )
  }
}

const translated = {
  viewMode: django.gettext('View mode'),
  viewList: django.gettext('View as list'),
  list: django.gettext('List'),
  viewMap: django.gettext('View as map'),
  map: django.gettext('Map')
}

export const ControlBarListMapSwitch = () => {
  const [queryParams, setQueryParams] = useSearchParams()
  const viewMode = queryParams.get('mode') || 'list'

  const handleClick = () => {
    queryParams.set('mode', viewMode === 'list' ? 'map' : 'list')
    setQueryParams(queryParams)
  }

  return (
    <div className="control-bar__list-map-switch-container">
      <span className="text--strong">{translated.viewMode}</span>
      <div className="control-bar__list-map-switch">
        <ViewModeButton
          active={viewMode === 'list'}
          handleClick={handleClick}
          aria-label={translated.viewList}
        >
          <span className="fa fa-list" aria-hidden="true" />&nbsp;
          {translated.list}
        </ViewModeButton>
        <ViewModeButton
          active={viewMode === 'map'}
          handleClick={handleClick}
          aria-label={translated.viewMap}
        >
          <span className="fa fa-map" aria-hidden="true" />&nbsp;
          {translated.map}
        </ViewModeButton>
      </div>
    </div>
  )
}
